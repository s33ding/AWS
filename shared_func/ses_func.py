import boto3
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Initialize the SES and S3 clients
ses_client = boto3.client('ses', region_name='us-east-1')
s3_client = boto3.client('s3')

# Step 1: Verify an Email Address in SES
def is_email_verified(email):
    response = ses_client.list_identities(IdentityType='EmailAddress')
    verified_emails = response['Identities']
    return email in verified_emails

def verify_email(email):
    if not is_email_verified(email):
        response = ses_client.verify_email_identity(EmailAddress=email)
        print(f"Verification email sent to {email}. Please check your inbox.")
    else:
        print(f"Email {email} is already verified.")

# Step 2: Download the S3 Object
def download_s3_object(bucket_name, object_key, download_path):
    s3_client.download_file(bucket_name, object_key, download_path)
    print(f"Downloaded {object_key} from bucket {bucket_name} to {download_path}")

# Step 3: Create the Email with Attachment
def create_email(sender_email, recipient_email, subject, body_text, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body_text, 'plain'))

    filename = os.path.basename(attachment_path)
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
        msg.attach(part)

    return msg

# Step 4: Send the Email via SES
def send_email(ses_client, sender_email, recipient_email, msg):
    response = ses_client.send_raw_email(
        Source=sender_email,
        Destinations=[recipient_email],
        RawMessage={'Data': msg.as_string()},
    )
    print("Email sent! Message ID:", response['MessageId'])
