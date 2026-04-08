import boto3
import sys
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, NoRegionError

# Constants
STACK_NAME = "my-ec2-stack"
TEMPLATE_FILE = "cloudformation-yaml/cloudformation-create-ec2.yml"

def create_stack(key_name):
    try:
        # Initialize CloudFormation client
        client = boto3.client('cloudformation')

        # Read the template file
        with open(TEMPLATE_FILE, 'r') as file:
            template_body = file.read()

        # Create CloudFormation stack
        print("Creating CloudFormation stack...")
        response = client.create_stack(
            StackName=STACK_NAME,
            TemplateBody=template_body,
            Parameters=[
                {
                    'ParameterKey': 'KeyName',
                    'ParameterValue': key_name
                }
            ]
        )

        # Display stack ID
        print("CloudFormation stack creation initiated. Stack ID:")
        print(response['StackId'])

    except FileNotFoundError:
        print(f"Error: Template file '{TEMPLATE_FILE}' not found.")
    except NoRegionError:
        print("Error: No AWS region found. Ensure that the region is set in your AWS configuration.")
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
    except PartialCredentialsError:
        print("Error: Partial AWS credentials found. Please check your AWS configuration.")
    except Exception as e:
        print(f"Error: {str(e)}")

def check_stack_status():
    try:
        # Initialize CloudFormation client
        client = boto3.client('cloudformation')

        # Describe the CloudFormation stack
        print("Checking the status of the stack...")
        response = client.describe_stacks(StackName=STACK_NAME)

        # Display stack information
        stack = response['Stacks'][0]
        print("Stack Name:", stack['StackName'])
        print("Stack Status:", stack['StackStatus'])
        print("Creation Time:", stack['CreationTime'])
        if 'Outputs' in stack:
            print("Outputs:")
            for output in stack['Outputs']:
                print(f"  {output['OutputKey']}: {output['OutputValue']}")

    except client.exceptions.ClientError as e:
        print(f"Error: {str(e)}")
    except NoRegionError:
        print("Error: No AWS region found. Ensure that the region is set in your AWS configuration.")
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
    except PartialCredentialsError:
        print("Error: Partial AWS credentials found. Please check your AWS configuration.")
    except Exception as e:
        print(f"Error: {str(e)}")

def delete_stack():
    try:
        # Initialize CloudFormation client
        client = boto3.client('cloudformation')

        # Delete the CloudFormation stack
        print("Deleting the CloudFormation stack...")
        client.delete_stack(StackName=STACK_NAME)

        print(f"CloudFormation stack '{STACK_NAME}' deletion initiated.")

    except client.exceptions.ClientError as e:
        print(f"Error: {str(e)}")
    except NoRegionError:
        print("Error: No AWS region found. Ensure that the region is set in your AWS configuration.")
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
    except PartialCredentialsError:
        print("Error: Partial AWS credentials found. Please check your AWS configuration.")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    print("Choose an option:")
    print("1. Create a new CloudFormation stack")
    print("2. Check the status of an existing stack")
    print("3. Delete the CloudFormation stack")
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        # Get the KeyName for the EC2 instance
        key_name = input("Enter the name of your existing EC2 KeyPair: ")
        if not key_name:
            print("Error: KeyPair name cannot be empty.")
            sys.exit(1)

        # Create the stack
        create_stack(key_name)

    elif choice == '2':
        # Check the stack status
        check_stack_status()

    elif choice == '3':
        # Delete the stack
        delete_stack()

    else:
        print("Invalid choice. Please run the script again and select either 1, 2, or 3.")
        sys.exit(1)

if __name__ == "__main__":
    main()

