import base64
import json

import boto3
from botocore.exceptions import ClientError
import mailtrap as mt


class EmailSender:
    def __init__(self):
        self.sender_email = 'mailtrap@zechem.net'

    def send_email_notification(self, to_email: str, subject: str, body_html: str):
        with open("src/assets/logo.jpeg", 'rb') as f:
            logo_content = f.read()

        mail = mt.Mail(
            sender=mt.Address(email=self.sender_email, name="Mailtrap"),
            to=[mt.Address(email=to_email, name="Customer")],
            subject=subject,
            html=body_html,
            category="Zechem",
            attachments=[
                mt.Attachment(
                    content=base64.b64encode(logo_content),
                    filename="logo.jpeg",
                    disposition=mt.Disposition.INLINE,
                    mimetype="image/jpeg",
                    content_id="logo.jpeg",
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
