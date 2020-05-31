from django import forms

from track.models import GuestVisit

from tempus_dominus.widgets import DateTimePicker


class GuestVisitForm(forms.ModelForm):

    arrival = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': True,
                'format': 'M/D/YY h:mm a',
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
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


class GuestVisitExportForm(forms.Form):

    FILE_TYPES = (
        ('C', 'CSV'),
        ('X', 'XLS')
    )

    file_type = forms.ChoiceField(
        choices=FILE_TYPES,
        label='File Type'
    )
    start = forms.DateTimeField(
        required=False,
        label='Start',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'placeholder': 'mm-dd-yyyy HH:MM PM',
        })
    )
    end = forms.DateTimeField(
        required=False,
        label='End',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'placeholder': 'mm-dd-yyyy HH:MM PM',
        })
    )