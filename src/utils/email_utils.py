import base64
import json

import boto3
from botocore.exceptions import ClientError
import mailtrap as mt
from src.utils.s3_utils import S3Utils


class EmailSender:
    def __init__(self):
        self.sender_email = 'mailtrap@zechem.net'
        self.s3 = S3Utils()

    def send_email_notification(self, to_email: str, subject: str, body_html: str):

        mail = mt.Mail(
            sender=mt.Address(email=self.sender_email, name="Zechem"),
            to=[mt.Address(email=to_email, name="Customer")],
            subject=subject,
            html=body_html,
            category="Zechem",
            attachments=[
                mt.Attachment(
                    content=base64.b64encode(
                        self.s3.download_picture_from_s3(bucket_name='logo-zechem', file_name='logo.jpeg')),
                    filename="logo.jpeg",
                    disposition=mt.Disposition.INLINE,
                    mimetype="image/jpeg",
                    content_id="logo",
                )
            ]
        )

        secret = self.get_mailtrap_secret()
        client = mt.MailtrapClient(token=secret["mailtrap_api_key"])
        client.send(mail)

    def get_mailtrap_secret(self):

        secret_name = "mailtrap"
        region_name = "eu-west-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        secret = get_secret_value_response['SecretString']

        return json.loads(secret)
