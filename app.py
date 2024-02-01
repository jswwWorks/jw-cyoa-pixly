import os
from dotenv import load_dotenv
import requests # TODO: will we need?

from s3_helpers import upload_to_s3

# load environment variables from .env file
load_dotenv()

import boto3

AWS_ACCESS_KEY = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BUCKET_NAME = os.environ['bucket_name']
REGION_CODE = os.environ['region_code']

from flask import Flask, request, render_template, flash, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES #TODO: do we need?
import exifread

from models import (
    Photo,
    connect_db
)

from s3_helpers import (
    photos_metadata_colname_conversions
)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['secret_key']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
debug = DebugToolbarExtension(app)


# attempt at configuring S3 connection, "manage via python" from lecture
s3 = boto3.client(
    's3',
    'us-east-1',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


@app.route('/', methods=['GET'])
def homepage():
    """Gets all photo_urls from s3 bucket and shows them on homepage."""

    print("in homepage route")

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

    return render_template('base.html', photos_urls=photos_urls)


@app.route('/upload', methods=['GET', 'POST'])
def upload_photo():
    """
    Grabs the metadata from a photo upload and then uploads the photo to the
    database.

    The GET route shows the upload form and the POST route processes form
    submission.

    While processing submission, gets file and grabs the metadata with the
    exifread library. Translates EXIF data names to corresponding
    column names in database.

    Also generates key in metadata for the file's name.

    Sends metadata to create a photo instance in the database with
    the appropriate metadata extracted from the photo upload. Then, resets
    cursor in process of reading document and calls function to upload the
    photo to the database.
    """

    if request.method == 'POST':
        file = request.files['photo']
        # after receiving valid photo file from form, we get a 'FileStorage'
        # object w/ methods and properties on it, most importantly, 'filename'.
        if file:
            tags = exifread.process_file(file)
            for tag in tags.keys():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                    print("Key: %s, value %s" % (tag, tags[tag]))

            metadata_tags = {}
            filename = file.filename
            metadata_tags["filename"] = filename

            for key, value in tags.items():
                if (
                    (key not in metadata_tags) and
                    (key in photos_metadata_colname_conversions)
                ):
                    conversion = photos_metadata_colname_conversions[key]
                    metadata_tags[conversion] = str(value)

            new_photo_in_db = Photo.submit_photo(metadata_tags)
            print('new_photo_in_db: ', new_photo_in_db)

            # puts cursor back to the beginning of the file
            file.seek(0)

            upload_to_s3(file, filename)
            # TODO: ^ this closes file
            flash('File uploaded successfully!')
            return redirect('/')
    return render_template('form.html')