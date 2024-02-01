import os
# from dotenv import load_dotenv
# import requests

from s3_helpers import upload_to_s3

# load environment variables from .env file
# load_dotenv()

import boto3
# s3 = boto3.resource('s3')

AWS_ACCESS_KEY = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BUCKET_NAME = os.environ['bucket_name']
# DATABASE_URL = os.environ['database_url']
REGION_CODE = os.environ['region_code']

from flask import Flask, request, render_template, flash, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
import exifread

from models import (
    photos_metadata_colname_conversions,
    Photo,
    connect_db,
    numeric_cols
)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['secret_key']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

print('database url: ', os.environ['DATABASE_URL'])

connect_db(app)

# Virtual-hosted–style requests
# https://<bucket-name>.s3.<region-code>.amazonaws.com/<key-name>


# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage

# from flask_debugtoolbar import DebugToolbarExtension

# import exifread <-- how to read exif data from photo file

# debug = DebugToolbarExtension(app)

# app.config['S3_BUCKET'] = 'S3_BUCKET_NAME'
# app.config['S3_KEY'] = 'AWS_ACCESS_KEY'
# app.config['S3_SECRET'] = 'AWS_ACCESS_SECRET'
# app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

photos = UploadSet("photos", IMAGES)


app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
configure_uploads(app, photos)


# attempt at configuring S3 connection, "manage via python" from lecture
s3 = boto3.client(
    's3',
    'us-east-1',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


@app.route('/', methods=['GET'])
def homepage():
    """Show homepage"""

    print("in homepage route")

    # Source: https://stackoverflow.com/questions/44238525/how-to-iterate-over-files-in-an-s3-bucket
    paginator = s3.get_paginator('list_objects_v2')
    # print(paginator)
    page_iterator = paginator.paginate(Bucket=BUCKET_NAME)
    # print("page iterator", page_iterator)


    photos_urls = []

    for page in page_iterator:
        # print("accessed a page")
        if page['KeyCount'] > 0:
            for file in page['Contents']:
                # print(file, "this is the file")
                # print(type(file))
                # print("this is the file name:", file["Key"])
                filename = file["Key"]
                # filename = file.filename
                photo_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com/{filename}'
                photos_urls.append(photo_url)


    # photo_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com/risotto.jpeg'





    return render_template('base.html', photos_urls=photos_urls)


@app.route('/upload', methods=['GET', 'POST'])
def upload_photo():
    if request.method == 'POST':
        # checks for file type
        file = request.files['photo']

        # print('This is file: ', file)
        # after receiving valid photo file from form, we get a 'FileStorage'
        # object w/ methods and properties on it, most importantly, 'filename'.
        if file:


# TODO: scaffolding code for extracting exif data from photos:
# attribution for exifread: https://pypi.org/project/ExifRead/

            # open image file for reading (must be in binary mode)
            # TODO: need exact path name of file being uploaded

            # file_path = os.path.abspath(file)
            # print('This is file_path: ', file_path)

            # photo_file = open(file_path, 'rb')

            # return exif tags
            # print('Before tags')
            tags = exifread.process_file(file)
            # print('After tags: ', tags)

            # for tag in tags.keys():
            #     if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            #         print("Key: %s, value %s" % (tag, tags[tag]))

            metadata_tags = {}

            for key, value in tags.items():
                if key not in metadata_tags and key in photos_metadata_colname_conversions:
                    conversion = photos_metadata_colname_conversions[key]
                    # print('This is conversion: ', conversion)

                    metadata_tags[conversion] = str(value)

                    # if conversion in numeric_cols: # converts to # in rare case
                    #     metadata_tags[conversion] = value

                    # print('metadata conversion for this entry', metadata_tags[conversion])

            print('metadata_tags before submit_photo: ', metadata_tags)


            print('This is metadata tags', metadata_tags)
            new_photo_in_db = Photo.submit_photo(metadata_tags)
            print('new_photo_in_db: ', new_photo_in_db)



            # if key in tags not in metadata_tags
            # and also check that it's in photos_metadata_colname_conversions:
            #     add key to metadata tags
            #     but before that, convert it using photos_metadata_colname_conversions







            filename = file.filename
            upload_to_s3(file, filename)
            flash('File uploaded successfully!')
            return redirect('/')
    return render_template('form.html')








# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         # checks for file type
#         if 'file' not in request.files:
#             return 'No file part'

#         file = request.files['file']

#         if file.filename == '':
#             return 'No selected file'

#         # if passes all checks, uploads file to S3 bucket
#         s3.upload_fileobj(file, 'name-of-bucket', file.filename)

#         flash("File uploaded successfully")

#     flash("Method not allowed. Failed to upload file.")