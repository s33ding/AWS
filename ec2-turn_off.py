import sys
from shared_func.ec2_func import turn_off_ec2

# Define lambda function to set default instance ID if not provided as an argument
instance_id_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input("Enter EC2 Instance ID to turn OFF: ")

# Get the instance ID using the lambda function
instance_id = instance_id_func()

# Turn off the EC2 instance
turn_off_ec2(instance_id)

