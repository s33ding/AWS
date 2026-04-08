from shared_func.kms_func import *
from shared_func.argv_parser import *
import json

test=1
if test:
    data = {"key":"value"}
    file_path = "data.json"
    output_path = "encrypted_data.json"

    with open (file_path , "w") as outfile:
        json.dump(data, outfile, indent=4)

    encrypt_file(
            file_path, 
            output_path, 
            key_alias=config.kms_key_alias, 
            session=session
            )


