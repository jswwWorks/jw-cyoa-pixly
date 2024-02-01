import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError


# load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BUCKET_NAME = os.environ['bucket_name']
REGION_CODE = os.environ['region_code']
SECRET_KEY = os.environ['secret_key']

LOCAL_FILE = 'test_file.txt'
NAME_FOR_S3 = 'test_file.txt'

print('This is region code', REGION_CODE)
print('This is secret key', SECRET_KEY)
print('This is bucket name', BUCKET_NAME)



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
    print('In upload fn')

    s3_client = boto3.client(
        service_name='s3',
        region_name=REGION_CODE,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    print('This is bucket name', BUCKET_NAME)

    print('This is file', file)
    print('This is filename', filename)

    resp = s3_client.upload_fileobj(file, BUCKET_NAME , filename)

    print(f'upload file response: {resp}')

    # boto closes file



def view_photos_from_s3():
    print('In view_photos_from_s3')