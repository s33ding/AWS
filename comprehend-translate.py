import boto3
import os
import json
import os
import time
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.comprehend_translate_func import comprehend_text
from shared_func.comprehend_translate_func import translate_text
from shared_func.argv_parser import get_input

# Read the AWS credentials from the JSON file
session = create_boto3_session()

text = get_input("text:")

lang_code = comprehend_text(text=text, session=session)

# Extract the language code from the Comprehend response
res = translate_text(text, lang_code, session=session)

print("\nsource language:",lang_code)
print("text:",text)
print("text translated:",res)
