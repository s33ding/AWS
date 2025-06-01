import boto3

# Create a Boto3 session
session = boto3.Session()

# Get the default region from the session
region = session.region_name

# Create an STS client using the session
sts_client = session.client('sts')

# Call get_caller_identity
identity = sts_client.get_caller_identity()

# Print the details
print("Account ID:", identity['Account'])
print("User ID:", identity['UserId'])
print("ARN:", identity['Arn'])
print("Region:", region)

