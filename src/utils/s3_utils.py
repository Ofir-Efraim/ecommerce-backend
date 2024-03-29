import base64
from urllib.parse import urlparse

import boto3


class S3Utils:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def upload_picture_to_s3(self, picture):
        # Upload picture file to S3 bucket
        bucket_name = 'zechem-products'
        file_name = picture.filename
        file_content = picture.read()
        # Upload file to S3
        response = self.s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_content,
            ContentEncoding='base64',
            ContentType=picture.content_type
        )

        # Generate URL for the uploaded picture
        picture_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        return picture_url

    def delete_picture_from_s3(self, picture_url):
        # Parse URL to get bucket name and file name
        parsed_url = urlparse(picture_url)
        bucket_name = parsed_url.netloc.split('.')[0]
        file_name = parsed_url.path.lstrip('/')

        # Delete file from S3 bucket

        response = self.s3_client.delete_object(
            Bucket=bucket_name,
            Key=file_name
        )
        return response

    def download_picture_from_s3(self, bucket_name: str, file_name: str):
        # Download file from S3 bucket
        response = self.s3_client.get_object(
            Bucket=bucket_name,
            Key=file_name
        )
        picture_content = response['Body'].read()

        return picture_content
