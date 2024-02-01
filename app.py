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
    photos_metadata_colname_conversions, upload_to_s3, view_photos_from_s3
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
    """Gets all photo_urls from s3 bucket and shows them on homepage."""

    print('Top of homepage route')

    # Gets searchbar submission and queries photos to display:
    searchCategory = request.args.get('search-category')
    searchTerm = request.args.get('search-term')

    print('searchCategory: ', searchCategory)
    print('searchTerm: ', searchTerm)

    col_name = searchCategory

    photos_urls = []
    if not searchTerm:
        photos_urls = view_photos_from_s3()
    else:

        # photos_urls = Photo.query.all() # this gave both photos
        # print("***query", Photo.query.all())


        photos_data = Photo.query.filter(Photo.filename.ilike("%Kodak%")).all()

        photos_urls = []

        for photo in photos_data:
            photo_url = photo.filename
            photos_urls.append(photo_url)

        # photos_urls = Photo.query.filter(Photo.filename.ilike(f"%{searchTerm}%"))

        # photos_urls = db.query(Photo).filter(Photo.__table__.c[col_name].like(f"%{searchTerm}%")).all()
        print('This is photo_urls: ', photos_urls)





        # photos_urls = Photo.query(Photo).filter(getattr(Photo, col_name).like(f"%{searchTerm}%")).all()
        # photos_urls = Photo.query(Notice).filter(Photo.searchCategory.like(f"%{searchTerm}%")).all()
        # photos_urls = Photo.query.filter(Photo.)
        # users = User.query.filter(User.username.like(f"%{search}%")).all()

    # TODO: query database w/ filtered search term
    # using filtered results, take the filename and get photos_urls from S3







    return render_template('base.html', photos_urls=photos_urls)


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
        # after receiving valid photo file from form, we get a 'FileStorage'
        # object w/ methods and properties on it, most importantly, 'filename'.
        if file:
            tags = exifread.process_file(file)

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