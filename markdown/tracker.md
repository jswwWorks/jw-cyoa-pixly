BUG LOG:
1. flask run bug w/ env variables
2. retrieving exif data that one would assume to be entirely numerical but is a different type (and converting it to a string makes it appear 'normal')
3. order of operations with file operations (attempted to retrieve EXIF data which caused I/O issues)

4. sqlalchemy.exc.DataError
sqlalchemy.exc.DataError: (psycopg2.errors.StringDataRightTruncation) value too long for type character varying(30)
from uploading lizard photo at 2:23am
-- one of the properties should have a longer varchar.

I believe it's the model. I'll try increasing that number and see if things work (I'm upping it to 60 characters)

that fixed the problem! Please reset your db so it can handle the new change

FIXME: added bug from Thurs w/ Joel's help
5. Python has attributes in dot notation, which means you can't get dicionary values using dot notation:

# getattr(o,"age",0)
# # obj, key, value if not found
# nums = [1, 2]
# nums.get(0)
^ Joel's Notes


6. I'm still getting sqlalchemy.exc.DataError when trying to upload a photo:
sqlalchemy.exc.DataError: (psycopg2.errors.StringDataRightTruncation) value too long for type character varying(30)

I can't tell what it is, maybe someone wrote a long description for exposure_time? I'm going to set a minimum of 60 characters for all fields just in case! Please let me know if that's too lenient for some columns and we can reduce those accordingly.

TODO: please reset your db so it gets the new changes! Thanks!!



VICTORY LOG:
1.