from django import forms
from contact_trace.custom_form_fields import CommaSeparatedEmailField

from users.models import CustomUser

from phonenumber_field.formfields import PhoneNumberField

from allauth.account.forms import SignupForm, LoginForm


class UserContactInfoForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        label='First Name'
    )
    last_name = forms.CharField(
        required=True,
        label='Last Name'
    )
    phone = PhoneNumberField(
        required=False,
        label='Phone Number'
    )

    password = None

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'phone'
        )


class InviteSingleUserForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        label='First Name'
    )
    last_name = forms.CharField(
        max_length=30,
        label='Last Name'
    )
    email = forms.EmailField(
        label='E-mail Address'
    )

    def create_user(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        user, new = CustomUser.objects.get_or_create(
            email=self.cleaned_data['email'],
        )
        if new:
            user.first_name = first_name,
            user.last_name = last_name,
            user.save()
        return user


class InviteUsersForm(forms.Form):

    emails = CommaSeparatedEmailField(
        label='E-mail Addresses',
        help_text='Please use a comma to separate email addresses'
    )
    invite_from = forms.CharField(
        max_length=500,
        label='From'
    )
    body = forms.CharField(
        label='Message',
        widget=forms.Textarea
    )


class RequestDemoForm(forms.Form):

    name = forms.CharField(
        max_length=200,
        label='Name'
    )
    email = forms.EmailField(
        label='E-mail'
    )
    email_2 = forms.CharField(
        max_length=500,
        label='',
        widget=forms.TextInput(attrs={'class': 'dispnon'}),
        required=False,
    )
    phone = PhoneNumberField(
        label='Phone'
    )
    company = forms.CharField(
        max_length=200,
        label='Company'
    )


class CustomSignupForm(SignupForm):

    class Meta(LoginForm):
        model = CustomUser
        fields = (
            'email',

        )
        exclude = (
            'username',
        )