#!/bin/bash

# Load the configuration file
config_file="$EC2_DS_CRED"
instance_id=`jq -r '.instance_id' $config_file`
region=`jq -r '.region' $config_file`

# Show menu
echo "1. Start EC2 Instance"
echo "2. Stop EC2 Instance"
read -p "Enter your choice [ 1 - 2] " choice

case $choice in
1)
    echo "Starting the EC2 Instance..."
    aws ec2 start-instances --instance-ids $instance_id --region $region
    ;;
2)
    echo "Stopping the EC2 Instance..."
    aws ec2 stop-instances --instance-ids $instance_id --region $region
    ;;
*)
    echo "Invalid option..."
    ;;
esac

