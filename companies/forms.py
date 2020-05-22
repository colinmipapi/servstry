from django import forms

from companies.models import WaitList


class WaitListForm(forms.ModelForm):

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your e-mail',
            }
        )
    )

    class Meta:
        model = WaitList
        fields = (
            'email',
        )
