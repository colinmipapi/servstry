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