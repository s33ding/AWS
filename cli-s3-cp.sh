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

# Prompt the user for whether to use the --recursive flag
read -p "Use --recursive flag? (y/n): " use_recursive

# Use the aws s3 cp command to copy files to or from the S3 bucket
if [ $sync_direction -eq 0 ]
then
  if [ "$use_recursive" == "y" ]
  then
    aws s3 cp "$source" "s3://$destination" --recursive
  else
    aws s3 cp "$source" "s3://$destination"
  fi
else
  if [ "$use_recursive" == "y" ]
  then
    aws s3 cp "s3://$source" "$destination" --recursive
  else
    aws s3 cp "s3://$source" "$destination"
  fi
fi
