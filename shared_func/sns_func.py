import boto3
import config

# Create an SNS client
sns_client = boto3.client('sns')

# Create an SNS topic
def create_sns_topic(topic_name):
    response = sns_client.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']
    print(f'Created topic with ARN: {topic_arn}')
    return topic_arn

# List all SNS topics
def list_sns_topics():
    
    response = sns_client.list_topics()
    topics = response['Topics']
    print('List of SNS Topics:')
    for topic in topics:
        print(topic['TopicArn'])
    return topics

# Subscribe an endpoint to a topic
def subscribe_to_topic(topic_arn, protocol, endpoint):
    """
    Subscribe an endpoint to an SNS topic with the specified protocol and endpoint.

    Args:
        topic_arn (str): The ARN of the SNS topic to subscribe to.
        protocol (str): The protocol for message delivery.
            - For email subscriptions, use 'email'.
            - For SMS subscriptions, use 'sms'.
            - For HTTPS/webhook subscriptions, use 'https'.
            - For AWS Lambda function subscriptions, use 'lambda'.
            - For Amazon SQS queue subscriptions, use 'sqs'.
            - For mobile app push notification subscriptions, use 'application'.
        endpoint (str): The destination endpoint based on the chosen protocol:
            - For 'email' protocol, provide an email address.
            - For 'sms' protocol, provide a phone number.
            - For 'https' protocol, provide the URL of the HTTP/HTTPS endpoint.
            - For 'lambda' protocol, provide the ARN of the AWS Lambda function.
            - For 'sqs' protocol, provide the ARN of the Amazon SQS queue.
            - For 'application' protocol, provide the platform-specific identifier for the mobile app.

    Returns:
        str: The ARN of the created subscription.
    """

    print(f"Subscribing to topic {topic_arn} with Protocol: {protocol} and Endpoint: {endpoint}")

    try:
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint
        )
        subscription_arn = response['SubscriptionArn']
        print(f'Successfully subscribed with ARN: {subscription_arn}')
        return subscription_arn
    except Exception as e:
        print(f'Error subscribing to topic {topic_arn}: {str(e)}')
        return None

# Publish a message to a topic
def publish_to_topic(topic_arn, message):
    
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    message_id = response['MessageId']
    print(f'Published message with ID: {message_id}')
    return message_id

# List subscriptions for a topic
def list_topic_subscriptions(topic_arn):
    
    response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    subscriptions = response['Subscriptions']
    print('Topic Subscriptions:')
    for subscription in subscriptions:
        print(subscription['SubscriptionArn'])
    return subscriptions

# Unsubscribe from a topic
def unsubscribe_from_topic(subscription_arn):
    
    sns_client.unsubscribe(SubscriptionArn=subscription_arn)
    print('Unsubscribed from the topic')

# Delete an SNS topic
def delete_sns_topic(topic_arn):
    
    sns_client.delete_topic(TopicArn=topic_arn)
    print(f'Deleted topic with ARN: {topic_arn}')

#if __name__ == '__main__':
#    topic_arn = create_sns_topic('MyTopicName')
#    list_sns_topics()
#    subscribe_arn = subscribe_to_topic(topic_arn, 'email', 'your.email@example.com')
#    message_id = publish_to_topic(topic_arn, 'Hello, world!')
#    list_topic_subscriptions(topic_arn)
#    unsubscribe_from_topic(subscribe_arn)

