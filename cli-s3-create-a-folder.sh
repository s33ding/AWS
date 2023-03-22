#!/bin/bash

CLOUD_ICON="☁️"

echo -e "${CLOUD_ICON} Enter bucket details:"
read -p "Bucket name: " bucket_name

echo -e "${CLOUD_ICON} Enter folder name:"
read -p "Folder name: " folder_name

echo -e "Make the folder public or private?"
echo -e "  0) Private (default)"
echo -e "  1) Public"
read -p "${CLOUD_ICON} > " is_public

if [ "$is_public" -eq 1 ]; then
    acl="--acl public-read"
else
    acl=""
fi

echo -e "${CLOUD_ICON} Creating folder..."
aws s3api put-object --bucket "$bucket_name" --key "$folder_name/" --content-length 0 $acl

echo -e "${CLOUD_ICON} Folder created successfully!" 
