import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

# load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BUCKET_NAME = os.environ['bucket_name']
REGION_CODE = os.environ['region_code']
SECRET_KEY = os.environ['secret_key']

LOCAL_FILE = 'test_file.txt'
NAME_FOR_S3 = 'test_file.txt'

print('This is region code', REGION_CODE)
print('This is secret key', SECRET_KEY)
print('This is bucket name', BUCKET_NAME)


def upload_to_s3(file, filename):
    print('In upload fn')

    s3_client = boto3.client(
        service_name='s3',
        region_name=REGION_CODE,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    print('This is bucket name', BUCKET_NAME)

    print('This is file', file)
    print('This is filename', filename)

    resp = s3_client.upload_fileobj(file, BUCKET_NAME , filename)

    print(f'upload file response: {resp}')



def view_photos_from_s3():
    print('In view_photos_from_s3')




# TODO: 1. view objects in bucket
        # 2. loop through objects in bucket
        # 3. per object in bucket, get the file and img src property
        # 4. render_template with "photo=photo_object" in def homepage()





# for testing individual file
# if __name__ == '__main__':
#     upload_to_s3()










#     {
# 	"Version": "2012-10-17",
# 	"Statement": [
# 		{
# 			"Sid": "Statement1",
# 			"Principal": "*",
# 			"Effect": "Allow",
# 			"Action": [
# 			    "s3:GetObject",
# 			    "s3:PutObject",
# 			    "s3:PutBucketPolicy"
# 			    ],
# 			"Resource": "arn:aws:s3:::cyoa-pixly-julia-carl/*"
# 		}
# 	]
# }