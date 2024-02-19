import boto3
from botocore.exceptions import ClientError


class SuppressionException(Exception):
    pass


class EmailSender:
    def __init__(self):
        # Create an SES client using the session
        self.ses_client = boto3.client('ses')
        self.sqs_client = boto3.client('sqs')
        self.bounce_queue_url = 'https://sqs.eu-west-1.amazonaws.com/851725256428/zechem_email_debounce'
        self.complaint_queue_url = 'https://sqs.eu-west-1.amazonaws.com/851725256428/zechem_email_complaints'

    def send_email_notification(self, to_email, subject, body_html):
        # Sender email address
        sender_email = 'zechem.gf@gmail.com'

        # Check if the email is in the suppression list (SQS queues for bounce or complaint notifications)
        if self._is_debounced(to_email) or self._is_complained(to_email):
            print(f"Email {to_email} is suppressed due to debounced or complaint.")
            self.add_to_ses_suppression_list(email=to_email)
            raise SuppressionException(f"Email {to_email} is suppressed due to bounce or complaint.")

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
        except:
            raise ClientError(
                {
                    'Error': {
                        'Code': '400',
                        'Message': 'Invalid email address'
                    }
                },
                operation_name='send_email'
            )
        else:
            print("Email sent! Message ID:", response['MessageId'])
            return True

    def _is_debounced(self, email):
        return self._check_queue(self.bounce_queue_url, email)

    def _is_complained(self, email):
        return self._check_queue(self.complaint_queue_url, email)

    def _check_queue(self, queue_url, email):
        try:
            # Receive messages from the SQS queue
            response = self.sqs_client.receive_message(
                QueueUrl=queue_url,
                AttributeNames=['All'],
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=10,
                WaitTimeSeconds=5
            )
            # Check if the email address is in the messages
            if 'Messages' in response:
                for message in response['Messages']:
                    # Check if the message body contains the email address
                    if 'Body' in message and email in message['Body']:
                        return True
            return False
        except Exception as e:
            print("Error checking queue:", e)
            return False

    def add_to_ses_suppression_list(self, email):
        try:
            response = self.ses_client.create_receipt_rule(
                RuleSetName='default',  # Use your rule set name
                Rule={
                    'Name': 'SuppressionRule',
                    'Enabled': True,
                    'TlsPolicy': 'Optional',
                    'Recipients': [email],
                    'Actions': [{'AddHeaderAction': {'HeaderName': 'X-SES-Suppression-List',
                                                     'HeaderValue': 'Bounced or Complaint'}}]
                }
            )
            print("Email added to SES suppression list:", email)
            return True
        except ClientError as e:
            print("Error adding email to SES suppression list:", e)
            return False
