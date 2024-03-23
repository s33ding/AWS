#!/bin/bash

CLOUD_ICON="☁️"

echo -e "${CLOUD_ICON} Enter bucket name to delete:"
read -p "${CLOUD_ICON} Bucket name: " bucket_name

echo -e "${CLOUD_ICON} Deleting bucket..."
aws s3 rb s3://$bucket_name --force
echo -e "${CLOUD_ICON} Bucket $bucket_name deleted."

echo -e "${CLOUD_ICON} Script completed."
