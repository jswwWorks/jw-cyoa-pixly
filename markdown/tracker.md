BUG LOG:
1. flask run bug w/ env variables
2. retrieving exif data that one would assume to be entirely numerical but is a different type (and converting it to a string makes it appear 'normal')
3. order of operations with file operations (attempted to retrieve EXIF data which caused I/O issues)


sqlalchemy.exc.DataError: (psycopg2.errors.StringDataRightTruncation) value too long for type character varying(30)
from uploading lizard photo at 2:23am
-- one of the properties should have a longer varchar.

I believe it's the model. I'll try increasing that number and see if things work (I'm upping it to 60 characters)

that fixed the problem! Please reset your db so it can handle the new change

VICTORY LOG:
1.