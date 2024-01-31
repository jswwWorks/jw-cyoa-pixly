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

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['secret_key']


# Virtual-hosted–style requests
# https://<bucket-name>.s3.<region-code>.amazonaws.com/<key-name>


# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage

# from flask_debugtoolbar import DebugToolbarExtension

# from sqlalchemy.exc import IntegrityError <-- db, not needed right now

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
    # TODO: attempt to retrieve photo(s) from S3 to put on homepage

    # Source: https://stackoverflow.com/questions/44238525/how-to-iterate-over-files-in-an-s3-bucket
    paginator = s3.get_paginator('list_objects_v2')
    print(paginator)
    page_iterator = paginator.paginate(Bucket=BUCKET_NAME)
    print("page iterator", page_iterator)


    photos_urls = []

    for page in page_iterator:
        print("accessed a page")
        if page['KeyCount'] > 0:
            for file in page['Contents']:
                print(file, "this is the file")
                print(type(file))
                # print("this is the file name:", file["Key"])
                filename = file["Key"]
                # filename = file.filename
                photo_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com/{filename}'
                photos_urls.append(photo_url)


    # photo_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com/risotto.jpeg'

    return render_template('base.html', photos_urls=photos)


@app.route('/upload', methods=['GET', 'POST'])
def upload_photo():
    if request.method == 'POST':
        # checks for file type
        file = request.files['photo']
        # after receiving valid photo file from form, we get a 'FileStorage'
        # object w/ methods and properties on it, most importantly, 'filename'.
        if file:
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