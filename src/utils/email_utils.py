import boto3
from botocore.exceptions import ClientError


class EmailSender:
    def __init__(self):
        # Create an SES client using the session
        self.ses_client = boto3.client('ses')

    def send_email_notification(self, to_email, subject, body_html):
        # Sender email address
        sender_email = 'zechem.gf@gmail.com'

        # Create a MIME formatted message
        message = {
            'Subject': {'Data': subject},
            'Body': {
                'Html': {'Data': body_html}
            }
        }

        # Send email using the SES client
        try:
            response = self.ses_client.send_email(
                Source=sender_email,
                Destination={'ToAddresses': [to_email]},
                Message=message
            )
        except ClientError as e:
            print("Error sending email:", e.response['Error']['Message'])
            return False
        else:
            print("Email sent! Message ID:", response['MessageId'])
            return True
