#!/bin/bash

# Load the configuration file
config_file="$EC2_CRED"
echo "$config_file"

instance_id=`jq -r '.instance_id' $config_file`
region=`jq -r '.region' $config_file`

echo "instance id: $instance_id"
echo "region: $region"

# Set your emoticon
emoticon="🖥️"

# Show menu
echo "1. Start EC2 Instance"
echo "2. Stop EC2 Instance"
echo "3. Check EC2 Instance Status"
prompt_message=" $emoticon  Enter your choice [ 1 - 3]:  "

echo ""
read -p "$prompt_message" choice

case $choice in
1)
    echo "Starting the EC2 Instance..."
    aws ec2 start-instances --instance-ids $instance_id --region $region
    ;;
2)
    echo "Stopping the EC2 Instance..."
    aws ec2 stop-instances --instance-ids $instance_id --region $region
    ;;
3)
    echo "Checking the EC2 Instance status..."
    aws ec2 describe-instances --instance-ids $instance_id --region $region --query "Reservations[*].Instances[*].State.Name" --output text
    ;;
*)
    echo "Invalid option..."
    ;;
esac

