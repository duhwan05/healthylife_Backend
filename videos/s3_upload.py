import boto3
import os
from django.conf import settings
from uuid import uuid4

def upload_file_to_s3(local_path, folder='analysis_videos'):
    ext = os.path.splitext(local_path)[-1]
    filename = f"{folder}/{uuid4().hex}{ext}"

    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    
    print(s3.list_buckets())
    with open(local_path, 'rb') as f:
        s3.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, filename)

    url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{filename}"
    return url
