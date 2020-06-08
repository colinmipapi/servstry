from django import forms
from django.contrib.auth.forms import UserCreationForm

from contact_trace.custom_form_fields import CommaSeparatedEmailField

from users.models import CustomUser

from phonenumber_field.formfields import PhoneNumberField

from allauth.account.forms import (
    SignupForm,
    LoginForm,
    SetPasswordForm,
    ChangePasswordForm
)
from allauth.socialaccount.forms import SignupForm as SocialSignupForm

from zxcvbn_password.fields import PasswordField, PasswordConfirmationField


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
        required=True,
        label='Phone Number'
    )
    create_business = forms.BooleanField(
        required=False,
        label='I need to create an account for my business'
    )

    password = None

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'phone'
        )


class NotificationSettings(forms.ModelForm):

    email_setting = forms.BooleanField(
        label='Receive all email notifications',
        required=False
    )

    class Meta:
        model = CustomUser
        fields = (
            'email_setting',
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

    password1 = PasswordField(
        label='Password'
    )
    password2 = PasswordConfirmationField(
        label='Confirm Password',
        confirm_with='password1'
    )

    class Meta(LoginForm):
        model = CustomUser
        fields = (
            'email',
        )


class CustomPasswordChangeForm(ChangePasswordForm):
    password1 = PasswordField(
        label='Password'
    )
    password2 = PasswordConfirmationField(
        label='Confirm Password',
        confirm_with='password1'
    )


class CustomSetPasswordForm(SetPasswordForm):
    password1 = PasswordField(
        label='Password'
    )
    password2 = PasswordConfirmationField(
        label='Confirm Password',
        confirm_with='password1'
    )


class CustomSocialSignupForm(SocialSignupForm):

    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    email = forms.EmailField(
        label='E-mail Address'
    )
    phone = PhoneNumberField(
        required=True,
        label='Phone Number'
    )
    password1 = PasswordField(
        label='Password'
    )
    password2 = PasswordConfirmationField(
        label='Confirm Password',
        confirm_with='password1'
    )
    create_business = forms.BooleanField(
        required=False,
        label='I also need to create an account for my business'
    )

    def signup(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.save()
        return user


class InvitationSignupForm(UserContactInfoForm):

    password = None
    email = forms.EmailField(
        label='E-mail',
        required=True
    )
    phone = PhoneNumberField(
        required=True,
        label='Phone Number'
    )
    password1 = PasswordField(
        label='Password'
    )
    password2 = PasswordConfirmationField(
        label='Confirm Password',
        confirm_with='password1'
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