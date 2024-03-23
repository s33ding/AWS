#!/bin/bash
#source: https://www.youtube.com/watch?v=Xv54k3TGoHM 

# Prompt user to select AWS key
echo "☁️  Select an AWS key:"
echo "  0) Work AWS key"
echo "  1) Personal AWS key"
read -p "> " aws_key_choice

if [ "$aws_key_choice" -eq 0 ]; then
  # Use work AWS key
  aws_key=$AWS_KEY_MAIN
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

echo "id: $id"

# Create formatted string
string="[default]\n\
aws_access_key_id=$id\n\
aws_secret_access_key=$secret"
# Store in file
touch ~/.aws/credentials
echo -e $string > $AWS_CRED

# Prompt for MFA token
read -p '☁️  TOKEN: ' -s TOKEN

# Get temporary credentials and format as JSON with new key names
aws=$(aws sts get-session-token --duration-seconds 30000 --serial-number $arn --token-code $TOKEN --output json)
echo "$aws" 
id=$(echo "$aws" | jq -r '.Credentials.AccessKeyId')
secret=$(echo "$aws" | jq -r '.Credentials.SecretAccessKey')
token=$(echo "$aws" | jq -r '.Credentials.SessionToken')
new_json=$(echo '{}' | jq --arg id "$id" --arg secret "$secret" --arg token "$token" '.id = $id | .secret = $secret | .token = $token')

# Write temporary credentials JSON to file
echo "$new_json" > "$AWS_TEMP_CRED"

# Remove existing credentials from file
> ~/.aws/credentials

# Rewrite AWS default credentials file with new values
echo "[default]" >> ~/.aws/credentials
echo "aws_access_key_id = $id" >> ~/.aws/credentials
echo "aws_secret_access_key = $secret" >> ~/.aws/credentials
echo "aws_session_token = $token" >> ~/.aws/credentials

# Display a fun message instead of the sensitive information
echo "Access granted."
echo "May the Bash be with you! 🚀👨💻🔥"

# Use AWS CLI with temporary credentials
aws s3 ls

