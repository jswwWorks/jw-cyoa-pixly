import os
from dotenv import load_dotenv
import boto3
import botocore
from models import Photo

from PIL import Image
from io import BytesIO


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

col_names = [
    "filename",
    "alt_tag",
    "make",
    "model",
    "orientation_rotation",
    "software",
    "date_and_time",
    "ycbcr_positioning",
    "x_resolution",
    "y_resolution",
    "resolution_unit",
    "exposure_time",
    "f_number",
    "exposure_program",
    "exif_version",
    "date_and_time_original",
    "date_and_time_digitized",
    "components_configuration",
    "exposure_bias",
    "metering_mode",
    "flash",
    "focal_length",
    "maker_note",
    "flashpix_version",
    "color_space",
    "interoperability_index",
    "interoperability_version"
]


def upload_to_s3(file, filename):
    """
    INPUT: Takes a file and a string of its name.

    FUNCTION: Uploads the file to a bucket in S3.

    OUTPUT: none
    """

    print('In upload_to_s3 function')

    try:
        resp = s3.upload_fileobj(file, BUCKET_NAME, filename)
    except botocore.exceptions.ClientError as error:
        raise error

    print(f'upload file response: {resp}')

    # boto closes file


def view_photos_from_s3():
    """Gets images from S3 bucket and returns a list of photo urls."""

    # Source: https://stackoverflow.com/questions/44238525/how-to-iterate-over-files-in-an-s3-bucket
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=BUCKET_NAME)

    base_aws_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com'

    photo_urls_alt_tags_filename = []

    for page in page_iterator:
        if page['KeyCount'] > 0:
            for file in page['Contents']:
                filename = file["Key"]
                photo_url = f'{base_aws_url}/{filename}'
                photo_instance = Photo.query.filter_by(filename=filename).one_or_none() # TRY
                # print("LOOK HERE", type(photo_instance))
                # print("this is our photo_instance", photo_instance)
                alt_tag = photo_instance.alt_tag


                photo_urls_alt_tags_filename.append(
                    (
                        photo_url,
                        alt_tag,
                        filename
                    )
                )

                # print("this is our alt tag", alt_tag)

    # print('This is zipped items: ', photo_urls_alt_tags_filename)

    return photo_urls_alt_tags_filename


def view_filtered_photos_from_s3(filenames):
    # paginator = s3.get_paginator('list_objects_v2')
    # page_iterator = paginator.paginate(Bucket=BUCKET_NAME)

    photo_urls_alt_tags_filename = []

    base_aws_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com'

    for file_name in filenames:
        photo_url = f'{base_aws_url}/{file_name}'

        # FIXME: removed unnecessary f strings (check elsewhere after this one)
        photo_instance = Photo.query.filter_by(filename=file_name).one_or_none()
        # TODO: ^ consolidate this repeated pattern into a separate helper fn

        alt_tag = photo_instance.alt_tag

        photo_urls_alt_tags_filename.append((photo_url, alt_tag, file_name))

    return photo_urls_alt_tags_filename



def edit_photo_and_save_to_s3(filename):
    """Downloads file from S3, makes photo edits, and saves file back to S3"""

    print('Inside edit_photo_and_save_to_s3')

    file_obj = BytesIO()

    s3.download_fileobj(BUCKET_NAME, filename, file_obj)

    file_obj.seek(0)

    image_to_be_edited = Image.open(file_obj)

    edited_image = image_to_be_edited.resize((300, 300))

    file_obj_edited = BytesIO()

    # FIXME: can only resize JPEG files currently, breaks on PNG files
    edited_image.save(file_obj_edited, format="JPEG")

    # This NEEDS to be here or else photo breaks
    file_obj_edited.seek(0)

    s3.upload_fileobj(file_obj_edited, BUCKET_NAME, filename)



# getattr(o,"age",0)
# # obj, key, value if not found

# nums = [1, 2]

# nums.get(0)