#!/bin/bash

# Exit on error
set -e

# --- Configuration ---
DIRECTORY_ID="d-1234567890"  # Replace with your actual Directory ID
USERNAME="$1"
NEW_PASSWORD="$2"

# --- Usage check ---
if [ -z "$USERNAME" ] || [ -z "$NEW_PASSWORD" ]; then
  echo "Usage: $0 <username> <new-password>"
  exit 1
fi

# --- AWS CLI Command ---
aws ds reset-user-password \
  --directory-id "$DIRECTORY_ID" \
  --user-name "$USERNAME" \
  --new-password "$NEW_PASSWORD"

echo "Password reset for user '$USERNAME' completed successfully."

