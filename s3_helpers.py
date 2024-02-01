import os
from dotenv import load_dotenv
import boto3
import botocore

# load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BUCKET_NAME = os.environ['bucket_name']
REGION_CODE = os.environ['region_code']
SECRET_KEY = os.environ['secret_key']

s3 = boto3.client(
    service_name='s3',
    region_name=REGION_CODE,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

photos_metadata_colname_conversions = {
    "Image Make": "make",
    "Image Model": "model",
    "Image Orientation": "orientation_rotation",
    "Image Software": "software",
    "Image DateTime": "date_and_time",
    "Image YCbCrPositioning": "ycbcr_positioning",
    "Image XResolution": "x_resolution",
    "Image YResolution": "y_resolution",
    "Image ResolutionUnit": "resolution_unit",
    "EXIF ExposureTime": "exposure_time",
    "EXIF FNumber": "f_number",
    "EXIF ExposureProgram": "exposure_program",
    "EXIF ExifVersion": "exif_version",
    "EXIF DateTimeOriginal": "date_and_time_original",
    "EXIF DateTimeDigitized": "date_and_time_digitized",
    "EXIF ComponentsConfiguration": "components_configuration",
    "EXIF ExposureBiasValue": "exposure_bias",
    "EXIF MeteringMode": "metering_mode",
    "EXIF Flash": "flash",
    "EXIF FocalLength": "focal_length",
    "EXIF UserComment": "maker_note",
    "EXIF FlashPixVersion": "flashpix_version",
    "EXIF ColorSpace": "color_space",
    "Interoperability InteroperabilityIndex": "interoperability_index",
    "Interoperability InteroperabilityVersion": "interoperability_version"
}

def upload_to_s3(file, filename):
    """
    INPUT: Takes a file and a string of its name.

    FUNCTION: Uploads the file to a bucket in S3.

    OUTPUT: none
    """

    print('In upload_to_s3 function')

    try:
        resp = s3.upload_fileobj(file, BUCKET_NAME , filename)
    except botocore.exceptions.ClientError as error:
        raise error

    print(f'upload file response: {resp}')

    # boto closes file


def view_photos_from_s3():
    """Gets images from S3 bucket and returns a list of photo urls."""

    # Source: https://stackoverflow.com/questions/44238525/how-to-iterate-over-files-in-an-s3-bucket
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=BUCKET_NAME)

    photos_urls = []

    # Original url:
    # photo_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com/{filename}'
    base_aws_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com'
    # Now, our photo_url will be f'{base_aws_url}/{filename}'

    for page in page_iterator:
        if page['KeyCount'] > 0:
            for file in page['Contents']:
                filename = file["Key"]
                photo_url = f'{base_aws_url}/{filename}'
                photos_urls.append(photo_url)

    return photos_urls