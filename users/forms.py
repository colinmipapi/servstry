from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from contact_trace.custom_form_fields import CommaSeparatedEmailField

from users.models import CustomUser

from phonenumber_field.formfields import PhoneNumberField

from allauth.account.forms import SignupForm, LoginForm


class EditUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email'
        )


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


class InvitationSignupForm(UserContactInfoForm):

    password = None
    email = forms.EmailField(
        label='E-mail',
        required=True
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone'
        )

        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = super(UserCreationForm, self).clean_password2()
            if password1 != password2:
                raise forms.ValidationError("Passwords must match")
            return password2


class ContactUsForm(forms.Form):

    full_name = forms.CharField(
        max_length=150,
        label='Full Name'
    )
    email_address = forms.EmailField(
        label='E-mail Address'
    )
    email_2 = forms.CharField(
        max_length=500,
        label='',
        widget=forms.TextInput(attrs={'class': 'dispnon'}),
        required=False,
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 5})
    )