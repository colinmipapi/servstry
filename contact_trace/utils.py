import sys

from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ExifTags
from io import BytesIO

def rotate_image(file):
    try:
        image = Image.open(file)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)

        buffer = BytesIO()
        image.save(buffer, format='JPEG', optimize=True, quality=85)
        new_image = InMemoryUploadedFile(buffer, None, file.name, file.content_type, sys.getsizeof(buffer), None)
        return new_image

    except:
            return file


def generate_unique_username(first_name, last_name):
    from users.models import CustomUser
    original = "%s%s" % (first_name, last_name)
    original = original.replace(" ", "")
    if CustomUser.objects.filter(username=original).exists():
        count = 1
        unique = False
        while not unique:
            original = "%s%i" % (original, count)
            if CustomUser.objects.filter(username=original).exists():
                count += 1
            else:
                return original
    else:
        return original