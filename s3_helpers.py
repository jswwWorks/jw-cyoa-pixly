import os
from dotenv import load_dotenv
import boto3

# load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BUCKET_NAME = os.environ['bucket_name']
REGION_CODE = os.environ['region_code']
SECRET_KEY = os.environ['secret_key']

LOCAL_FILE = 'test_file.txt'
NAME_FOR_S3 = 'test_file.txt'

def upload():
    print('In upload fn')

    s3_client = boto3.client(
        service_name='s3',
        region_name=REGION_CODE,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    resp = s3_client.upload_file(LOCAL_FILE, BUCKET_NAME , NAME_FOR_S3)

    print(f'upload file response: {resp}')