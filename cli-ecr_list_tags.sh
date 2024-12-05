#!/bin/bash

REPOSITORY_NAME="data-prophets"
AWS_REGION="us-east-1"

# List the images in the specified ECR repository
echo "Fetching tags for repository: $REPOSITORY_NAME in region: $AWS_REGION"

# Get the image tags
TAGS=$(aws ecr list-images --repository-name "$REPOSITORY_NAME" --region "$AWS_REGION" --query 'imageIds[*].imageTag' --output json)

# Check if TAGS is empty
if [ "$TAGS" == "[]" ]; then
    echo "No tags found in repository $REPOSITORY_NAME."
else
    # Parse and print tags
    echo "Tags in repository $REPOSITORY_NAME:"
    echo "$TAGS" | jq -r '.[]'
fi

