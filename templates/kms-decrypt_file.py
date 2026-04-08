from shared_func.kms_func import *
from shared_func.argv_parser import *
import json
import os

test=1
if test:
    data = {"key":"value"}
    file_path = "data.json"
    output_path = "encrypted_data.json"

    with open (file_path , "w") as outfile:
        json.dump(data, outfile, indent=4)

    print("sv:", file_path)
    print("encrypting:", output_path)

    encrypt_file(
            file_path,
            output_path,
            key_alias=config.kms_key_alias
            )

    encrypted_file_path = "encrypted_data.json"
    output_path = "decrypted_data.json"

    print("decrypting:", output_path)
    decrypt_file(
            encrypted_file_path, 
            output_path
            )

delete=1
if delete:

    file_path = "data.json"
    encrypted_file_path = "encrypted_data.json"
    output_path = "decrypted_data.json"

    for fl in [file_path, encrypted_file_path, output_path]:
        print("deleting:", fl)
        os.system(f"rm -f {fl}")
            


