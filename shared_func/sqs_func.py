import os
import boto3

# Specify the region
aws_region = 'us-east-1'

# Function to create an SQS queue
def create_sqs_queue(queue_name):
    sqs = boto3.client('sqs', region_name=aws_region)
    response = sqs.create_queue(QueueName=queue_name)
    return response['QueueUrl']

# Function to send a message to an SQS queue
def send_message_to_queue(queue_url, message_body):
    sqs = boto3.client('sqs', region_name=aws_region)
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    return response['MessageId']

# Function to receive messages from an SQS queue
def receive_messages_from_queue(queue_url, num_messages=1):
    sqs = boto3.client('sqs', region_name=aws_region)
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=num_messages,
        MessageAttributeNames=['All'],
        WaitTimeSeconds=20  # Adjust as needed
    )
    messages = response.get('Messages', [])
    return messages

# Function to delete a message from an SQS queue
def delete_message_from_queue(queue_url, receipt_handle):
    sqs = boto3.client('sqs', region_name=aws_region)
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

def delete_sqs_queue(queue_url, aws_region):
    sqs = boto3.client('sqs', region_name=aws_region)
    try:
        sqs.delete_queue(QueueUrl=queue_url)
        print(f"Deleted SQS queue with URL: {queue_url}")
    except Exception as e:
        print(f"An error occurred while deleting the queue: {str(e)}")

# Function to get the approximate number of messages in a queue
def get_approximate_message_count(queue_url):
    sqs = boto3.client('sqs', region_name=aws_region)
    response = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['ApproximateNumberOfMessages']
    )
    return int(response['Attributes']['ApproximateNumberOfMessages'])

def list_sqs_queues():
    # Initialize the SQS client
    sqs = boto3.client('sqs')
    
    # List all available queues
    response = sqs.list_queues()
    
    # Extract and print the queue URLs
    if 'QueueUrls' in response:
        queue_urls = response['QueueUrls']
        for url in queue_urls:
            print(f"Queue URL: {url}")
    else:
        print("No queues found.")

