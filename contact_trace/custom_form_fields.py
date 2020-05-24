from django import forms
from django.core.validators import validate_email, EMPTY_VALUES
from django.forms.fields import Field


class CommaSeparatedEmailField(Field):
    description ="E-mail address(es)"

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop("token", ",")
        super(CommaSeparatedEmailField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return []

        value = [item.strip() for item in value.split(self.token) if item.strip()]

        return list(set(value))

    def clean(self, value):
        """
        Check that the field contains one or more 'comma-separated' emails
        and normalizes the data to a list of the email strings.
        """
        value = self.to_python(value)

        if value in EMPTY_VALUES and self.required:
            raise forms.ValidationError("This field is required.")

        for email in value:
            try:
                validate_email(email)
                print(validate_email(email))
            except forms.ValidationError:
                error = "%s' is not a valid e-mail address." % (email)
                raise forms.ValidationError(error)
        return value