from shared_func.kms_func import *
from shared_func.argv_parser import *

secret = get_input(message='Please enter a value: ')

print("secret:", secret)

res = encrypt_string(secret, key_alias=config.kms_key_alias)

print("secret encrypted:", res)

