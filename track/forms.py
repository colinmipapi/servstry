from django import forms

from track.models import GuestVisit


class GuestVisitForm(forms.ModelForm):
    arrival = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'placeholder': 'mm-dd-yyyy HH:MM PM',
        })
    )

    class Meta:

        model = GuestVisit
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'arrival'
        )


class GuestVisitFilterForm(forms.Form):

    start = forms.DateTimeField(
        required=False,
        label='',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'placeholder': 'mm-dd-yyyy HH:MM PM',
        })
    )
    end = forms.DateTimeField(
        required=False,
        label='',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'placeholder': 'mm-dd-yyyy HH:MM PM',
        })
    )