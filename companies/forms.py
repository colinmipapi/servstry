import re

from django import forms

from contact_trace.utils import rotate_image

from contact_trace.validators import validate_image_extension

from companies.models import Company, WaitList, STATES

from phonenumber_field.formfields import PhoneNumberField


class WaitListForm(forms.ModelForm):

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter email address',
            }
        ),
        error_messages={
            'required': 'Please enter a valid email address'
        }
    )

    class Meta:
        model = WaitList
        fields = (
            'email',
        )


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = (
            'name',
        )


class NameAddressForm(forms.ModelForm):

    name = forms.CharField(
        label="Company Name"
    )
    address1 = forms.CharField(
        required=True,
        label="Address One"
    )
    address2 = forms.CharField(
        required=False,
        label="Address Two"
    )
    city = forms.CharField(
        required=True
    )
    state = forms.ChoiceField(
        required=True,
        choices=STATES
    )
    zip_code = forms.CharField(
        required=True,
        label="Zip Code"
    )

    class Meta:
        model = Company
        fields = (
            'name',
            'address1',
            'address2',
            'city',
            'state',
            'zip_code',
        )


class ContactInfoForm(forms.ModelForm):
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'id': 'phoneNumber',
        }),
        label="Phone",
    )
    website = forms.URLField(
        max_length=200,
        initial="https://",
        widget=forms.TextInput
    )

    class Meta:
        model = Company
        fields = (
            'phone',
            'website',
        )


# Add & Edit Company Logo Img
class LogoForm(forms.ModelForm):

    logo = forms.FileField(
        required=False,
        validators=[validate_image_extension],
        widget=forms.FileInput(attrs={
            'class': 'custom-file-input',
            'id': 'logoInp',
        }),
    )
    logo_background_color = forms.CharField(
        required=False,
        label='',
        help_text='Please enter a valid hex color (i.e. #fff)',
        widget=forms.TextInput({
            'placeholder': "#FAFAFA",
        })
    )

    class Meta:
        model = Company
        fields = (
            'logo',
            'logo_background_color'
        )
        labels = {
            "logo": "",
            "logo_background_color": "",
        }

    def clean_logo(self):
        img_raw = self.cleaned_data.get('logo')
        img = rotate_image(img_raw)
        return img

    def clean_logo_background_color(self):
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', self.cleaned_data.get('logo_background_color'))
        if match or self.cleaned_data.get('logo_background_color') == '':
            return self.cleaned_data.get('logo_background_color')
        else:
            raise forms.ValidationError("Not a valid hex color")


# Add & Edit Company Cover Img
class CoverImgForm(forms.ModelForm):

    cover_img = forms.FileField(
        required=True,
        validators=[validate_image_extension],
        widget=forms.FileInput(attrs={
            'class': 'custom-file-input',
            'id': 'coverImgInp',
        }),
    )

    class Meta:
        model = Company
        fields = (
            'cover_img',
        )
        labels = {
            "cover_img": "",
        }

    def clean_cover_img(self):
        img_raw = self.cleaned_data.get('cover_img')
        img = rotate_image(img_raw)
        return img


# Edit Company
class EditCompanyInfoForm(forms.ModelForm):
    name = forms.CharField(
        label="Company Name"
    )
    address1 = forms.CharField(
        required=True,
        label="Address One"
    )
    address2 = forms.CharField(
        required=False,
        label="Address Two"
    )
    city = forms.CharField(
        required=True
    )
    state = forms.ChoiceField(
        required=True,
        choices=STATES
    )
    zip_code = forms.CharField(
        required=True,
        label="Zip Code"
    )
    website = forms.URLField(
        max_length=200,
        initial="https://",
        widget=forms.TextInput
    )
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'id': 'phoneNumber',
        }),
        label="Phone",
        required=False,
    )

    class Meta:
        model = Company
        fields = (
            'name',
            'address1',
            'address2',
            'city',
            'state',
            'zip_code',
            'website',
            'phone'
        )
