CREATE TABLE photos_metadata (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(150) UNIQUE,
    make VARCHAR(60),
    model VARCHAR(60),
    orientation_rotation VARCHAR(60),
    software VARCHAR(60),
    date_and_time VARCHAR(60),
    ycbcr_positioning VARCHAR(60),
    x_resolution VARCHAR(60),
    y_resolution VARCHAR(60),
    resolution_unit VARCHAR(60),
    exposure_time VARCHAR(60),
    f_number VARCHAR(60),
    exposure_program VARCHAR(60),
    exif_version VARCHAR(60),
    date_and_time_original VARCHAR(60),
    date_and_time_digitized VARCHAR(60),
    components_configuration VARCHAR(60),
    exposure_bias VARCHAR(60),
    metering_mode VARCHAR(60),
    flash VARCHAR(100),
    focal_length VARCHAR(60),
    maker_note VARCHAR(100),
    flashpix_version VARCHAR(60),
    color_space VARCHAR(60),
    interoperability_index VARCHAR(60),
    interoperability_version VARCHAR(50),
    alt_tag VARCHAR(400));


-- Aight, look. We type coerced everything into only strings because it's difficult trying to convert
-- Idftag (?) types into float/num for columns that needed those types. Somehow, just converting them
-- from Idftag to string made the column data work, so we're sticking with that. And that's final.
-- Sorry.

-- If you know how to convert Idftag to float/num successfully, please let us know.