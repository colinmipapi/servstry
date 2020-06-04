from storages.backends.s3boto3 import S3Boto3Storage


class ProfileImageMediaStorage(S3Boto3Storage):
    location = 'media/company/profile-images'
    file_overwrite = False


class CoverImageMediaStorage(S3Boto3Storage):
    location = 'media/company/cover-images'
    file_overwrite = False


class FlyerMediaStorage(S3Boto3Storage):
    location = 'media/company/flyers'
    file_overwrite = True