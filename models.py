"""SQLAlchemy models for pixly app"""

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


class Photo(db.Model):
    """Photo in the database."""

    __tablename__ = "photos_metadata"
    # Note to selves: this is how we link our model to the database table!

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    filename = db.Column(
        db.String(150),
        nullable=True,
        unique=True,
    )

    make = db.Column(
        db.String(60),
        nullable=True,
    )

    model = db.Column(
        db.String(60),
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
        db.String(50),
        nullable=True,
    )

    flash = db.Column(
        db.String(100),
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
        db.String(50),
        nullable=True,
    )

    interoperability_index = db.Column(
        db.String(10),
        nullable=True,
    )

    interoperability_version = db.Column(
        db.String(50),
        nullable=True,
    )

    alt_tag = db.Column(
        db.String(400),
        nullable=False
    )

    @classmethod
    def submit_photo(self, metadata_tags):
        """
        INPUTS: submit_photo takes its instance and it takes metadata_tags,
        a dictionary with information on a photo's metadata.

        metadata_tags example:
        {
            filename: "Kodak_CX7530.jpg",
            make: "EASTMAN KODAK COMPANY",
            model: "KODAK CX7530 ZOOM DIGITAL CAMERA",
            ...
        }

        FUNCTION: generates a new instance of Photo class using metadata_tags.
        Adds photo instance to database.

        OUTPUT: new_photo, the generated instance of the photograph.
        """

        print('This is metadata_tags: ', metadata_tags)

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
