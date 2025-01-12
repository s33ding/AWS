import boto3
import sys
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import pandas as pd

# Initialize the EC2 client
ec2_client = boto3.client('ec2')

def create_key_pair(key_name, save_path):
    try:
        # Create a key pair
        response = ec2_client.create_key_pair(KeyName=key_name)

        # Extract the private key
        private_key = response['KeyMaterial']

        # Save the private key to a file
        key_file_path = os.path.join(save_path, f"{key_name}.pem")
        with open(key_file_path, 'w') as key_file:
            key_file.write(private_key)

        # Set file permissions to read-only
        os.chmod(key_file_path, 0o400)

        print(f"Key pair '{key_name}' created and saved to {key_file_path}")
        return key_file_path
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def get_instance_name(tags):
    """Extracts the Name tag from the instance tags."""
    if tags:
        for tag in tags:
            if tag['Key'] == 'Name':
                return tag['Value']
    return "Unnamed"

def list_ec2(return_list=False):
    """Lists all EC2 instances with their name, status, and type."""
    try:
        response = ec2_client.describe_instances()
        instances = []
        print("\nAvailable EC2 Instances:")
        print(f"{'Index':<5}{'Name':<25}{'Instance ID':<20}{'State':<15}{'Type':<15}")
        print("-" * 80)

        index = 1
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                instance_type = instance['InstanceType']
                name = get_instance_name(instance.get('Tags'))
                print(f"{index:<5}{name:<25}{instance_id:<20}{state:<15}{instance_type:<15}")
                instances.append((name, instance_id, state, instance_type))
                index += 1

        if return_list:
            return instances
    except Exception as e:
        print(f"Error listing EC2 instances: {e}")

def select_instance():
    """Displays a menu to select an EC2 instance."""
    instances = list_ec2(return_list=True)
    if not instances:
        print("No EC2 instances found.")
        return None
    
    print("\nSelect an instance:")
    for index, (name, instance_id, state, instance_type) in enumerate(instances):
        print(f"{index + 1}. Name: {name}, Instance ID: {instance_id}, State: {state}, Type: {instance_type}")

    while True:
        try:
            choice = int(input("Enter the number of the instance: ")) - 1
            if 0 <= choice < len(instances):
                return instances[choice][1]  # Return the selected instance ID
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def delete_ec2(instance_id):
    """Deletes an EC2 instance by ID."""
    try:
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"Terminating instance {instance_id}: {response}")
    except Exception as e:
        print(f"Error deleting EC2 instance {instance_id}: {e}")

def turn_off_ec2(instance_id):
    """Stops an EC2 instance by ID."""
    try:
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        print(f"Stopping instance {instance_id}: {response}")
    except Exception as e:
        print(f"Error stopping EC2 instance {instance_id}: {e}")

def turn_on_ec2(instance_id):
    """Starts an EC2 instance by ID."""
    try:
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        print(f"Starting instance {instance_id}: {response}")
    except Exception as e:
        print(f"Error starting EC2 instance {instance_id}: {e}")

def menu_to_control():
    """Menu to control EC2 instances interactively."""
    while True:
        print("\nEC2 Control Menu")
        print("1. List EC2 Instances")
        print("2. Delete EC2 Instance")
        print("3. Turn Off EC2 Instance")
        print("4. Turn On EC2 Instance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            list_ec2()
        elif choice == '2':
            instance_id = select_instance()
            if instance_id:
                delete_ec2(instance_id)
        elif choice == '3':
            instance_id = select_instance()
            if instance_id:
                turn_off_ec2(instance_id)
        elif choice == '4':
            instance_id = select_instance()
            if instance_id:
                turn_on_ec2(instance_id)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")



def list_ec2_instances():
    try:
        # Initialize a session using Amazon EC2
        ec2_client = boto3.client('ec2')

        # Describe all instances
        response = ec2_client.describe_instances()

        # Extract instance details
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance.get('InstanceId', 'N/A')
                public_ip = instance.get('PublicIpAddress', 'N/A')
                private_ip = instance.get('PrivateIpAddress', 'N/A')
                state = instance.get('State', {}).get('Name', 'N/A')
                public_dns = instance.get('PublicDnsName', 'N/A')
                instance_link = f"https://console.aws.amazon.com/ec2/v2/home?region={ec2_client.meta.region_name}#Instances:instanceId={instance_id}"

                instances.append({
                    'Instance ID': instance_id,
                    'State': state,
                    'Public IP': public_ip,
                    'Private IP': private_ip,
                    'Public DNS': public_dns,
                    'Instance Link': instance_link
                })

        # Create a DataFrame from the instance list
        df = pd.DataFrame(instances)

        # Display the DataFrame
        print("EC2 Instances:")
        print(df)

        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def list_and_manage_key_pairs():
    try:
        # Initialize a session using Amazon EC2
        ec2_client = boto3.client('ec2')

        # Retrieve all key pairs
        response = ec2_client.describe_key_pairs()

        # Extract key pair details
        key_pairs = []
        for key_pair in response['KeyPairs']:
            key_name = key_pair.get('KeyName', 'N/A')
            key_fingerprint = key_pair.get('KeyFingerprint', 'N/A')

            key_pairs.append({
                'Key Name': key_name,
                'Fingerprint': key_fingerprint
            })

        # Create a DataFrame for display
        df = pd.DataFrame(key_pairs)

        if df.empty:
            print("No key pairs found.")
            return

        print("Available Key Pairs:")
        print(df)

        # Interactive menu for deletion
        while True:
            print("\nOptions:")
            print("1. Delete a key pair")
            print("2. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                key_to_delete = input("Enter the Key Name to delete: ").strip()

                # Check if the key exists in the list
                if key_to_delete in df['Key Name'].values:
                    try:
                        ec2_client.delete_key_pair(KeyName=key_to_delete)
                        print(f"Key pair '{key_to_delete}' has been deleted.")

                        # Remove from the DataFrame
                        df = df[df['Key Name'] != key_to_delete]
                        print("Updated Key Pairs:")
                        print(df)

                        if df.empty:
                            print("No more key pairs remaining.")
                            break
                    except Exception as e:
                        print(f"An error occurred while deleting the key pair: {e}")
                else:
                    print("Key name not found in the list.")

            elif choice == '2':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {e}")
