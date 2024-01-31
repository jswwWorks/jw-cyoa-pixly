"""SQLAlchemy models for pixly app"""


from datetime import datetime

db = SQLAlchemy()


class Photo(db.Model):
    """Photo in the database."""

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    filename = db.Column(
        db.String(150),
        nullable=True,
    )

    manufacturer = db.Column(
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
        db.DateTime,
        nullable=True,
    )

    ycbcr_positioning = db.Column(
        db.String(30),
        nullable=True,
    )

    compression = db.Column(
        db.String(50),
        nullable=True,
    )

    x_resolution = db.Column(
        db.Numeric(10, 2),
        nullable=True,
    )

    y_resolution = db.Column(
        db.Numeric(10, 2),
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
        db.DateTime,
        nullable=True,
    )

    date_and_time_digitized = db.Column(
        db.DateTime,
        nullable=True,
    )

    components_configuration = db.Column(
        db.String(25),
        nullable=True,
    )

    compressed_bits_per_pixel = db.Column(
        db.Numeric(10, 2),
        nullable=True,
    )

    exposure_bias = db.Column(
        db.Numeric(2, 2),
        nullable=True,
    )

    maximum_aperture_value = db.Column(
        db.Numeric(10, 2),
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

    pixel_x_dimension = db.Column(
        db.Integer,
        nullable=True,
    )

    pixel_y_dimension = db.Column(
        db.Integer,
        nullable=True,
    )

    file_source = db.Column(
        db.String(10),
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
    def submit_photo(**kwargs):

        print('This is **kwargs: ', kwargs)

        # test print for keyword args passed into fn
        for key, value in kwargs.items():
            print("%s == %s" % (key, value))


        print('Before new photo')
        new_photo = Photo(kwargs)
        print('After new photo: ', new_photo)

        db.session.add(new_photo)

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