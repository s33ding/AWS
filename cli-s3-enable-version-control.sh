#!/bin/bash

# Prompt the user for the bucket name
read -p "Enter the S3 bucket name: " bucket_name

# Check if the bucket name is not empty
if [ -z "$bucket_name" ]; then
  echo "Bucket name cannot be empty. Exiting."
  exit 1
fi

# Enable versioning on the specified bucket
echo "Enabling versioning on bucket: $bucket_name"
aws s3api put-bucket-versioning --bucket "$bucket_name" --versioning-configuration Status=Enabled

# Verify the versioning status
echo "Verifying versioning status..."
versioning_status=$(aws s3api get-bucket-versioning --bucket "$bucket_name")

# Output the result
echo "Versioning status for bucket '$bucket_name':"
echo "$versioning_status"

