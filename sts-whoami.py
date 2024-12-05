import boto3

# Create an STS client
sts_client = boto3.client('sts')

# Call get_caller_identity
identity = sts_client.get_caller_identity()

# Print the details
print("Account ID:", identity['Account'])
print("User ID:", identity['UserId'])
print("ARN:", identity['Arn'])

