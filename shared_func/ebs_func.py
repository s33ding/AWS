import boto3
from botocore.exceptions import ClientError

ec2_client = boto3.client('ec2')

def create_volume(size, availability_zone, tag_value='true'):
    try:
        response = ec2_client.create_volume(
            Size=size,
            AvailabilityZone=availability_zone,
            TagSpecifications=[
                {
                    'ResourceType': 'volume',
                    'Tags': [
                        {
                            'Key': 'Temporary',
                            'Value': tag_value
                        }
                    ]
                }
            ]
        )
        print(f"Created volume: {response['VolumeId']}")
        return response['VolumeId']
    except ClientError as e:
        print(e)
        return None

def delete_volume(volume_id):
    try:
        ec2_client.delete_volume(VolumeId=volume_id)
        print(f"Deleted volume: {volume_id}")
    except ClientError as e:
        print(e)

def attach_volume(volume_id, instance_id, device):
    try:
        response = ec2_client.attach_volume(
            VolumeId=volume_id,
            InstanceId=instance_id,
            Device=device
        )
        print(f"Attached volume: {response['VolumeId']} to instance: {instance_id}")
    except ClientError as e:
        print(e)

def detach_volume(volume_id):
    try:
        response = ec2_client.detach_volume(VolumeId=volume_id)
        print(f"Detached volume: {response['VolumeId']}")
        return True
    except ClientError as e:
        print(e)
        return False

# Example usage:
def manage_volume(size, availability_zone, instance_id, device):
    # Create a 10 GB volume in the 'us-west-2a' availability zone
    volume_id = create_volume(size=size, availability_zone=availability_zone)
    
    if volume_id:
        # Attach the volume to an instance
        attach_volume(volume_id=volume_id, instance_id=instance_id, device=device)
        
        # Wait for the volume to be attached (this could be enhanced by adding a waiter)
        input("Press Enter after verifying the volume is attached...")

        # Detach the volume from the instance
        if detach_volume(volume_id=volume_id):
            # Wait for the volume to be detached (this could be enhanced by adding a waiter)
            input("Press Enter after verifying the volume is detached...")
            
            # Delete the volume
            delete_volume(volume_id=volume_id)

# Run the example with specific parameters
#manage_volume(size=10, availability_zone='us-west-2a', instance_id='i-1234567890abcdef0', device='/dev/sdf')

