from django.core.exceptions import ValidationError

from contact_trace.utils import rotate_image


def validate_image_extension(value):
    file_type_list = [
        'image/jpg',
        'image/png',
        'image/jpeg'
    ]

    try:
        if value:
            file_type = value.content_type
            if file_type in file_type_list:
                return value.file
            else:
                raise ValidationError(u'Not a valid file type (jpg, png, jpeg)')
    except:
        raise ValidationError(u'Not a valid file type (jpg, png, jpeg)')


def validate_file_extension(value):
    file_type_list = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]

    try:
        if value.file:
            file_type = value.file.content_type

            if file_type not in file_type_list:
                raise ValidationError(u'Not a valid file type (doc, docx, pdf)')

    except(AttributeError):
        pass

    return value.file