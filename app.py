import os
from dotenv import load_dotenv
import requests

# load environment variables from .env file
load_dotenv()

import boto3
# s3 = boto3.resource('s3')

AWS_ACCESS_KEY = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BUCKET_NAME = os.environ['bucket_name']
# DATABASE_URL = os.environ['database_url']
REGION_CODE = os.environ['region_code']
SECRET_KEY = os.environ['secret_key']


# Virtual-hosted–style requests
# https://<bucket-name>.s3.<region-code>.amazonaws.com/<key-name>

from flask import Flask, request, render_template, flash
from flask_uploads import UploadSet, configure_uploads, IMAGES

# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage

# from flask_debugtoolbar import DebugToolbarExtension

# from sqlalchemy.exc import IntegrityError <-- db, not needed right now

# import exifread <-- how to read exif data from photo file

app = Flask(__name__)
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
    'us-west-1',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


@app.route('/', methods=['GET'])
def homepage():
    """Show homepage"""

    # TODO: attempt to retrieve photo(s) from S3 to put on homepage




    photo_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com/pixly-photos/chowder.jpeg'

    return render_template('base.html', photo_url=photo_url)










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



def upload():
    print('In upload fn')

    s3_client = boto3.client(
        service_name='s3',
        region_name=REGION_CODE,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    resp = s3_client.upload_file(LOCAL_FILE, BUCKET_NAME , NAME_FOR_S3)

    print(f'upload file response: {resp}')