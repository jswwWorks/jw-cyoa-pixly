"""SQLAlchemy models for pixly app"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)


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

numeric_cols = ["x_resolution", "y_resolution", "exposure_bias"]


class Photo(db.Model):
    """Photo in the database."""

    __tablename__ = "photos_metadata"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    filename = db.Column(
        db.String(150),
        nullable=True,
    )

    make = db.Column(
        db.String(60),
        nullable=True,
    )

    model = db.Column(
        db.String(30),
        nullable=True,
    )

    orientation_rotation = db.Column(
        db.String(30),
        nullable=True,
    )

    software = db.Column(
        db.String(30),
        nullable=True,
    )

    date_and_time = db.Column(
        db.String(30),
        nullable=True,
    )

    ycbcr_positioning = db.Column(
        db.String(30),
        nullable=True,
    )

    x_resolution = db.Column(
        db.String(30),
        nullable=True,
    )

    y_resolution = db.Column(
        db.String(30),
        nullable=True,
    )

    resolution_unit = db.Column(
        db.String(25),
        nullable=True,
    )

    exposure_time = db.Column(
        db.String(15),
        nullable=True,
    )

    f_number = db.Column(
        db.String(10),
        nullable=True,
    )

    exposure_program = db.Column(
        db.String(30),
        nullable=True,
    )

    exif_version = db.Column(
        db.String(30),
        nullable=True,
    )

    date_and_time_original = db.Column(
        db.String(30),
        nullable=True,
    )

    date_and_time_digitized = db.Column(
        db.String(30),
        nullable=True,
    )

    components_configuration = db.Column(
        db.String(25),
        nullable=True,
    )

    exposure_bias = db.Column(
        db.String(30),
        nullable=True,
    )

    metering_mode = db.Column(
        db.String(20),
        nullable=True,
    )

    flash = db.Column(
        db.String(40),
        nullable=True,
    )

    focal_length = db.Column(
        db.String(10),
        nullable=True,
    )

    maker_note = db.Column(
        db.String(100),
        nullable=True,
    )

    flashpix_version = db.Column(
        db.String(35),
        nullable=True,
    )

    color_space = db.Column(
        db.String(20),
        nullable=True,
    )

    interoperability_index = db.Column(
        db.String(10),
        nullable=True,
    )

    interoperability_version = db.Column(
        db.String(20),
        nullable=True,
    )

    @classmethod
    def submit_photo(self, metadata_tags):

        print('This is metadata_tags: ', metadata_tags)

        # test print for keyword args passed into fn
        # for key, value in args.items():
        #     print("%s == %s" % (key, value))


        print('Before new photo')
        try:
            new_photo = Photo(**metadata_tags)
            print('After new photo: ', new_photo)
            print('new_photo.make: ', new_photo.make)
        except IntegrityError:
            print('error occurred', IntegrityError)


        db.session.add(new_photo)

        db.session.commit()

        return new_photo


        # Warbler code for reference:
        # )

        #     user = User(
        #     username=username,
        #     email=email,
        #     password=hashed_pwd,
        #     image_url=image_url,
        # )

        # db.session.add(user)
        # return user

