#!/bin/bash
#source: https://www.youtube.com/watch?v=Xv54k3TGoHM 


# Prompt user to select AWS key
echo "☁️  Select an AWS key:"
echo "  0) Work AWS key"
echo "  1) Personal AWS key"
read -p "> " aws_key_choice

if [ "$aws_key_choice" -eq 0 ]; then
  # Use work AWS key
  aws_key=$AWS_KEY
elif [ "$aws_key_choice" -eq 1 ]; then
  # Use personal AWS key
  aws_key=$AWS_KEY2
else
  echo "Invalid choice. Exiting."
  exit 1
fi

# Read the json file and extract the id and secret values
id=$(jq -r '.id' "$aws_key")
secret=$(jq -r '.secret' "$aws_key")
arn=$(jq -r '.arn' "$aws_key")
#
# Create formatted string
string="[default]\n\
aws_access_key_id = $id\n\
aws_secret_access_key = $secret"
# Store in file

touch ~/.aws/credentials
echo -e $string > $AWS_CRED
read -p '☁️  TOKEN: ' -s TOKEN

aws sts get-session-token --duration-seconds 4600 --serial-number  $arn --token-code $TOKEN > $AWS_TEMP_CRED

# Load temporary credentials from file
aws=$(jq -r '.Credentials' "$AWS_TEMP_CRED")

# Create credentials file
echo -e "[default]\n\
aws_access_key_id=$(echo "$aws" | jq -r '.AccessKeyId')\n\
aws_secret_access_key=$(echo "$aws" | jq -r '.SecretAccessKey')\n\
aws_security_token=$(echo "$aws" | jq -r '.SessionToken')" > "$AWS_CRED"

# Display a fun message instead of the sensitive information
echo "Access granted."
echo "May the Bash be with you! 🚀👨💻🔥"
aws s3 ls 
