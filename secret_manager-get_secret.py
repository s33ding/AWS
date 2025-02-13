import sys
import json
import os
from shared_func.argv_parser import get_input
from shared_func.secret_manager_func import get_secret

def main():
    # Get inputs
    secret_name = get_input("secret_name: ")
    res = get_secret(secret_name)

    # Check if the secret is a JSON string and parse it
    if isinstance(res, str):
        try:
            res = json.loads(res)
        except json.JSONDecodeError:
            print("Secret is not in JSON format. Displaying as a string:")
            print(res)
            return

    # Display the secret in a formatted way
    print("\nRetrieved Secret:")
    for key, value in res.items():
        print(f"- {key}: {value}")

    # Check if second argument is provided and equals "1"
    if len(sys.argv) > 2 and sys.argv[2] == "1":
        # Ensure tmp directory exists
        os.makedirs("tmp", exist_ok=True)
        secret_file_path = "/tmp/secret-manager.json"
        
        try:
            # Save secret as JSON file
            with open(secret_file_path, "w") as secret_file:
                json.dump(res, secret_file, indent=4)

            print(f"\n✅ Secret saved to {secret_file_path}")

        except Exception as e:
            print(f"\n❌ Error saving secret to file: {e}")

if __name__ == "__main__":
    main()

