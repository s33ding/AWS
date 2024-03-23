#!/bin/bash

# Define computer and cloud icons
computer_icon="🖥️"
cloud_icon="☁️"

# Prompt the user for the synchronization direction
read -p "Enter the synchronization direction (0 = local to S3, 1 = S3 to local): " sync_direction

# Prompt the user for the local directory path and S3 bucket name/folder path
if [ $sync_direction -eq 0 ]
then
  source_path="$computer_icon  Enter the local directory path: "
  destination_path="$cloud_icon  Enter the S3 bucket name and folder path: "
else
  source_path="$cloud_icon  Enter the S3 bucket name and folder path: "
  destination_path="$computer_icon  Enter the local directory path: "
fi

read -p "$source_path" source
read -p "$destination_path" destination

# Use the aws s3 sync command to synchronize the local directory with the S3 bucket
if [ $sync_direction -eq 0 ]
then
  aws s3 sync "$source" "s3://$destination"
else
  aws s3 sync "s3://$source" "$destination"
fi

