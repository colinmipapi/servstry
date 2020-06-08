from django import forms

from track.models import (
    GuestVisit,
    CustomSafetyPolicy
)

from tempus_dominus.widgets import DateTimePicker
from tinymce.widgets import TinyMCE


class GuestVisitForm(forms.ModelForm):

    arrival = forms.DateTimeField(
        input_formats=["%m/%d/%y %I:%M %p"],
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': True,
                'format': 'M/D/YY h:mm A',
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
    safety_policy_accept = forms.BooleanField(
        required=True
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


class UserVisitForm(forms.ModelForm):

    arrival = forms.DateTimeField(
        input_formats=["%m/%d/%y %I:%M %p"],
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': True,
                'format': 'M/D/YY h:mm A',
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
    safety_policy_accept = forms.BooleanField(
        required=True
    )

    class Meta:

        model = GuestVisit
        fields = (
            'user',
            'arrival'
        )
        widgets = {
            'user': forms.HiddenInput(),
        }


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


class CustomSafetyPolicyForm(forms.ModelForm):

    policy_text = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
    )

    class Meta:

        model = CustomSafetyPolicy
        fields = (
            'policy_text',
        )
