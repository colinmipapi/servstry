from allauth.account.forms import LoginForm, SignupForm
from django.shortcuts import redirect


class LoginFormMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)  # Call process_request()
        response = self.get_response(request)
        return response

    def process_request(self, request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = LoginForm()

        request.login_form = form


class SignUpFormMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)  # Call process_request()
        response = self.get_response(request)
        return response

    def process_request(self, request):
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = SignupForm()

        request.signup_form = form
