#!/bin/bash

CLOUD_ICON="☁️"

echo -e "${CLOUD_ICON} Enter bucket details:"
read -p "Bucket name: " bucket_name

echo -e "Make the bucket public or private?"
echo -e "  0) Private (default)"
echo -e "  1) Public"
read -p "${CLOUD_ICON} > " is_public

if [ "$is_public" -eq 1 ]; then
    acl="--acl public-read"
else
    acl=""
fi

echo -e "${CLOUD_ICON} Creating bucket..."
aws s3api create-bucket --bucket "$bucket_name" $acl

echo -e "${CLOUD_ICON} Bucket created successfully!"
