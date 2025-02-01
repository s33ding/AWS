import sys
from shared_func.sns_func import *


# Define lambda function to set default user name if not provided as an argument
topic_arn_func= lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the topic arn: "
)

# Function to select the protocol
def protocol_func():
    if len(sys.argv) > 2:
        return sys.argv[2]
    else:
        while True:
            print("""
            Select a protocol for message delivery:
            1. Email (email)
            2. SMS (sms)
            3. HTTPS/Webhook (https)
            4. AWS Lambda (lambda)
            5. Amazon SQS (sqs)
            6. Mobile App Push Notification (application)
            """)

            choice = input("Enter the number of the protocol: ")
            
            if choice == '1':
                return 'email'
            elif choice == '2':
                return 'sms'
            elif choice == '3':
                return 'https'
            elif choice == '4':
                return 'lambda'
            elif choice == '5':
                return 'sqs'
            elif choice == '6':
                return 'application'
            else:
                print("Invalid choice. Please select a valid option.")

# Function to select the endpoint
def endpoint_func():
    if len(sys.argv) > 3:
        return sys.argv[3]

    while True:
        if protocol == 'email':
            return input("Enter the email address for the endpoint: ")
        elif protocol == 'sms':
            return input("Enter the phone number for the endpoint: ")
        elif protocol == 'https':
            return input("Enter the URL of the HTTP/HTTPS endpoint: ")
        elif protocol == 'lambda':
            return input("Enter the ARN of the AWS Lambda function: ")
        elif protocol == 'sqs':
            return input("Enter the ARN of the Amazon SQS queue: ")
        elif protocol == 'application':
            return input("Enter the platform-specific identifier for the mobile app: ")
        else:
            print("Invalid protocol. Please provide a valid protocol.")


# Example usage of protocol_func
topic_arn = topic_arn_func()
protocol = protocol_func()
endpoint = endpoint_func()

# Get the user name using the lambda function
subscription_arn = subscribe_to_topic(topic_arn, protocol, endpoint)
