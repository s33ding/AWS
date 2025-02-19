import sys
import json
import os
import argparse
from shared_func.secret_manager_func import create_secret

def validate_json_file(file_path):
    """Checks if the JSON file exists and is valid."""
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json.load(file)  # Ensure it's valid JSON
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' contains invalid JSON.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Create a secret from a JSON file.")
    parser.add_argument("secret_name", nargs="?", help="Name of the secret")
    parser.add_argument("json_path", nargs="?", help="Path to the JSON file")

    args = parser.parse_args()

    if not args.secret_name:
        args.secret_name = input("Enter the secret name: ").strip()
    
    if not args.json_path:
        args.json_path = input("Enter the JSON file path: ").strip()

    # Validate JSON file
    validate_json_file(args.json_path)

    try:
        response = create_secret(args.secret_name, args.json_path)
        print("✅ Secret Created Successfully:", response)
    except Exception as e:
        print(f"❌ Error creating secret: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

