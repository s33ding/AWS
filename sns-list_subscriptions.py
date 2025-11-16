import boto3

sns = boto3.client('sns')
response = sns.list_subscriptions()

for subscription in response['Subscriptions']:
    print(f"Topic: {subscription['TopicArn']}")
    print(f"Protocol: {subscription['Protocol']}")
    print(f"Endpoint: {subscription['Endpoint']}")
    print(f"Status: {subscription['SubscriptionArn']}")
    print("-" * 50)
