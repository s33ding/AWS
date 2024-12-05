from shared_func.kms_func import *
from shared_func.argv_parser import *

test = 1
if test:
    secret = "testing KMS"
    print("secret:", secret)
    res = encrypt_string(secret, key_alias=config.kms_key_alias, session=session)
    encrypted_secret = res

print("encrypted secret:", encrypted_secret)

res = decrypt_string(encrypted_secret, key_alias=config.kms_key_alias, session=session)

print("secret decrypted:", res)

