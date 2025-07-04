import json
import boto3
import logging

# Create SQS client at module level to reuse connection across invocations
sqs = boto3.client('sqs')

# Configure your logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# SQS queue URL (make configurable if you like)
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/248189947068/test-sqs-queue"

def forward_sns_to_sqs(event, context, queue_url=SQS_QUEUE_URL):
    """
    Generic Lambda handler to forward SNS messages to an SQS queue.
    """
    logger.info("Received event: %s", json.dumps(event))

    for record in event.get('Records', []):
        try:
            # Extract SNS message
            sns_message = record['Sns']['Message']
            logger.info("SNS Message: %s", sns_message)

            # Optionally: parse if JSON
            try:
                parsed_message = json.loads(sns_message)
                logger.info("Parsed SNS Message: %s", json.dumps(parsed_message))
                message_body = json.dumps(parsed_message)
            except json.JSONDecodeError:
                # If not JSON, just use the raw string
                message_body = sns_message

            # Send to SQS
            response = sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=message_body
            )

            logger.info("Sent message to SQS. MessageId: %s", response.get('MessageId'))

        except Exception as e:
            logger.error("Error processing record: %s", e, exc_info=True)

