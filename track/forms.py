from django import forms

from track.models import GuestVisit

from tempus_dominus.widgets import DateTimePicker


class GuestVisitForm(forms.ModelForm):

    arrival = forms.DateTimeField(
        input_formats=["%m/%d/%y %H:%M %p"],
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
    email_2 = forms.CharField(
        max_length=500,
        label='',
        widget=forms.TextInput(attrs={'class': 'dispnon'}),
        required=False,
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

    start_filter = forms.DateTimeField(
        input_formats=["%m/%d/%y %H:%M %p"],
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
        label='',
        required=False
    )
    end_filter = forms.DateTimeField(
        input_formats=["%m/%d/%y %H:%M %p"],
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
        label='',
        required=False
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
    start_export = forms.DateTimeField(
        input_formats=["%m/%d/%y %H:%M %p"],
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
        label='Start',
        required=False
    )
    end_export = forms.DateTimeField(
        input_formats=["%m/%d/%y %H:%M %p"],
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
        label='End',
        required=False
    )
