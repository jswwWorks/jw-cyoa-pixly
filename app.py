import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

import boto3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

AWS_ACCESS_KEY = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BUCKET_NAME = os.environ['bucket_name']
REGION_CODE = os.environ['region_code']

from flask import Flask, request, render_template, flash, redirect
import exifread

from models import (
    Photo,
    connect_db
)

from s3_helpers import (
    photos_metadata_colname_conversions,
    upload_to_s3,
    view_photos_from_s3,
    view_filtered_photos_from_s3,
    col_names
)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['secret_key']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

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


@app.route('/', methods=['GET', 'POST'])
def homepage():
    """
    Shows homepage.

    The GET route gets all photo_urls from the s3 bucket and displays them on
    the homepage.

    The POST route handles the submission of a search in the database for photos
    matching a particular search term. Users can select a column in the database
    to search by along with a search term. Populates the homepage only with
    photo(s) matching the search term.
    """

    print('Top of homepage route')

    photo_urls_alt_tags_filename = []

    if request.method == 'GET':
        photo_urls_alt_tags_filename = view_photos_from_s3()

        print('This is zipped items in app: ', photo_urls_alt_tags_filename)
        return render_template(
            'gallery.html',
            col_names=col_names,
            photo_urls_alt_tags_filename=photo_urls_alt_tags_filename
        )

    search_category = request.form['search-category']
    search_term = request.form['search-term']
    # print('searchCategory: ', search_category)
    # print('searchTerm: ', search_term)

    photos_data = Photo.query.filter(
        getattr(Photo, search_category).ilike(f"%{search_term}%")).all()

    filenames = []

    for photo in photos_data:
        photo_filename = photo.filename
        filenames.append(photo_filename)

    photo_urls_alt_tags_filename = view_filtered_photos_from_s3(filenames)
    flash(f'Showing results for {search_term}')

    return render_template(
        'gallery.html',
        photo_urls_alt_tags_filename=photo_urls_alt_tags_filename,
        col_names=col_names
    )


@app.route('/photos/<filename>', methods=['GET', 'POST'])
def get_single_photo(filename):
    """
    Route function that gets single photo and shows all of its metadata
    information.

    Can make edits on photo (<-- figure this out later)
    """
    print('get_single_photo filename: ', filename)


    if request.method == 'GET':

        # FIXME: this is breaking
        photo = Photo.query.filter_by(filename=f'{filename}').one_or_none()
        print("our new photo!!!", photo)
        print('This is photo.filename: ', photo.filename)

        print('this is filename_test')



        photo_metadata = []

        # TODO: assemble an
        # for col in col_names:
        #     print(col, "!!!!!!!!!!!!!!!!!!!!!!!!!")
        #     photo_metadata.append(photo.get(f"{col}"))

        print("this is metadata", photo_metadata)

        base_aws_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com'
        photo_url = f'{base_aws_url}/{photo.filename}'

        return render_template(
            'photo.html',
            photo=photo,
            photo_url=photo_url,
            photo_metadata=photo_metadata
        )


@app.route('/upload', methods=['GET', 'POST'])
def upload_photo():
    """
    Grabs the metadata from a photo upload and then uploads the photo to the
    database.

    The GET route shows the upload form and the POST route processes form
    submission.

    While processing submission, gets file and grabs the metadata via the
    exifread library. Translates EXIF data names to corresponding
    column names in database.

    Also generates a key in metadata for the file's name.

    Uses metadata extracted from the photo upload to create a photo instance
    in the database. Then, resets cursor in photo file uploads the
    photo to the database.
    """

    if request.method == 'POST':
        file = request.files['photo']
        alt_tag = request.form['alt-tag']
        print("new alt tag,", alt_tag)
        # after receiving valid photo file from form, we get a 'FileStorage'
        # object w/ methods and properties on it, most importantly, 'filename'.
        if file:
            tags = exifread.process_file(file)

            metadata_tags = {}
            filename = file.filename
            metadata_tags["filename"] = filename
            metadata_tags["alt_tag"] = alt_tag or filename

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
            # ^ this closes file
            flash('File uploaded successfully!')
            return redirect('/')
    return render_template('form.html')