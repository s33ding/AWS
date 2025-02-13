import sys
import json
from shared_func.secret_manager_func import create_secret

def main():
    if len(sys.argv) < 3:
        secret_name = input("Enter the secret name: ").strip()
        json_file = input("Enter the json file path: ").strip()
    else:
        secret_name = sys.argv[1]
        json_file_path = sys.argv[2]


    response = create_secret(secret_name, json_file_path)
    print("Secret Created Successfully:", response)

if __name__ == "__main__":
    main()
  
