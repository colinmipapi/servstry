var elements = stripe.elements();

var style = {
  base: {
    color: "#32325d",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4"
    }
  },
  invalid: {
    color: "#fa755a",
    iconColor: "#fa755a"
  }
};


var cardElement = elements.create("card", { style: style });

$(document).ready(function() {
    cardElement.mount("#card-element");

    cardElement.on('change', showCardError)
});

function showCardError(event) {
  let displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function createPaymentMethod(cardElement, customerId, priceId) {
  return stripe
    .createPaymentMethod({
      type: 'card',
      card: cardElement,
    })
    .then((result) => {
      if (result.error) {
        console.log(result);
        displayError(error);
      } else {
        createSubscription({
          customerId: customerId,
          paymentMethodId: result.paymentMethod.id,
          priceId: priceId,
        });
      }
    });
}

function createSubscription(customerId, paymentMethodId, priceId) {
  return (
    fetch('/api/billing/create-subscription/', {
      method: 'POST',
      credentials: "same-origin",
       headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Accept": "application/json",
          'Content-Type': 'application/json'
       },
      body: JSON.stringify({
        customerId: customerId,
        paymentMethodId: paymentMethodId,
        priceId: priceId,
      }),
    })
      .then((response) => {
        return response.json();
      })
      // If the card is declined, display an error to the user.
      .then((result) => {
        if (result.error) {
          // The card had an error when trying to attach it to a customer.
          throw result;
        }
        return result;
      })
      // Normalize the result to contain the object returned by Stripe.
      // Add the addional details we need.
      .then((result) => {
        return {
          paymentMethodId: paymentMethodId,
          priceId: priceId,
          subscription: result,
        };
      })
      // Some payment methods require a customer to be on session
      // to complete the payment process. Check the status of the
      // payment intent to handle these actions.
      .then(handleCustomerActionRequired)
      // If attaching this card to a Customer object succeeds,
      // but attempts to charge the customer fail, you
      // get a requires_payment_method error.
      .then(handlePaymentMethodRequired)
      // No more actions required. Provision your service for the user.
      .then(onSubscriptionComplete)
      .catch((error) => {
        // An error has happened. Display the failure to the user here.
        // We utilize the HTML element we created.
        showCardError(error);
      })
  );
}

function handleCustomerActionRequired({
  subscription,
  invoice,
  priceId,
  paymentMethodId,
  isRetry,
}) {
  if (subscription && subscription.status === 'active') {
    // Subscription is active, no customer actions required.
    return { subscription, priceId, paymentMethodId };
  }

  // If it's a first payment attempt, the payment intent is on the subscription latest invoice.
  // If it's a retry, the payment intent will be on the invoice itself.
  let paymentIntent = invoice ? invoice.payment_intent : subscription.latest_invoice.payment_intent;

  if (
    paymentIntent.status === 'requires_action' ||
    (isRetry === true && paymentIntent.status === 'requires_payment_method')
  ) {
    return stripe
      .confirmCardPayment(paymentIntent.client_secret, {
        payment_method: paymentMethodId,
      })
      .then((result) => {
        if (result.error) {
          // Start code flow to handle updating the payment details.
          // Display error message in your UI.
          // The card was declined (i.e. insufficient funds, card has expired, etc).
          throw result;
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            // Show a success message to your customer.
            // There's a risk of the customer closing the window before the callback.
            // We recommend setting up webhook endpoints later in this guide.
            return {
              priceId: priceId,
              subscription: subscription,
              invoice: invoice,
              paymentMethodId: paymentMethodId,
            };
          }
        }
      })
      .catch((error) => {
        displayError(error);
      });
  } else {
    // No customer action needed.
    return { subscription, priceId, paymentMethodId };
  }
}

function handlePaymentMethodRequired({
  subscription,
  paymentMethodId,
  priceId,
}) {
  if (subscription.status === 'active') {
    // subscription is active, no customer actions required.
    return { subscription, priceId, paymentMethodId };
  } else if (
    subscription.latest_invoice.payment_intent.status ===
    'requires_payment_method'
  ) {
    // Using localStorage to manage the state of the retry here,
    // feel free to replace with what you prefer.
    // Store the latest invoice ID and status.
    localStorage.setItem('latestInvoiceId', subscription.latest_invoice.id);
    localStorage.setItem(
      'latestInvoicePaymentIntentStatus',
      subscription.latest_invoice.payment_intent.status
    );
    throw { error: { message: 'Your card was declined.' } };
  } else {
    return { subscription, priceId, paymentMethodId };
  }
}

function retryInvoiceWithNewPaymentMethod(
  customerId,
  paymentMethodId,
  invoiceId,
  priceId
) {
  return (
    fetch('/api/billing/retry-invoice/', {
      method: 'POST',
      credentials: "same-origin",
       headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Accept": "application/json",
          'Content-Type': 'application/json'
       },
      body: JSON.stringify({
        customerId: customerId,
        paymentMethodId: paymentMethodId,
        invoiceId: invoiceId,
      }),
    })
      .then((response) => {
        return response.json();
      })
      // If the card is declined, display an error to the user.
      .then((result) => {
        if (result.error) {
          // The card had an error when trying to attach it to a customer.
          throw result;
        }
        return result;
      })
      // Normalize the result to contain the object returned by Stripe.
      // Add the addional details we need.
      .then((result) => {
        return {
          // Use the Stripe 'object' property on the
          // returned result to understand what object is returned.
          invoice: result,
          paymentMethodId: paymentMethodId,
          priceId: priceId,
          isRetry: true,
        };
      })
      // Some payment methods require a customer to be on session
      // to complete the payment process. Check the status of the
      // payment intent to handle these actions.
      .then(handlePaymentThatRequiresCustomerAction)
      // No more actions required. Provision your service for the user.
      .then(onSubscriptionComplete)
      .catch((error) => {
        // An error has happened. Display the failure to the user here.
        // We utilize the HTML element we created.
        displayError(error);
      })
  );
}

function cancelSubscription(subscriptionId) {
  return fetch('/api/billing/cancel-subscription/', {
    method: 'POST',
    credentials: "same-origin",
    headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Accept": "application/json",
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      subscriptionId: subscriptionId,
    }),
  })
    .then(response => {
      return response.json();
    })
    .then(cancelSubscriptionResponse => {
      // Display to the user that the subscription has been cancelled.
    });
}