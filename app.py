import os

from flask import Flask, request, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES

# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage

from flask_debugtoolbar import DebugToolbarExtension
# from sqlalchemy.exc import IntegrityError <-- db, not needed right now

# import exifread <-- how to read exif data from photo file

app = Flask(__name__)

photos = UploadSet("photos", IMAGES)


app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
configure_uploads(app, photos)




@app.route('/', methods=['GET'])
def homepage():
    """Show homepage"""

    return render_template('homepage.html')
