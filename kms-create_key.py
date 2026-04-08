from shared_func.kms_func import *
from shared_func.argv_parser import *

key_nm = input("key_name:")
description = input("description:")
create_kms_key(description=description , alias_name=f"alias/{key_nm}" , key_usage='ENCRYPT_DECRYPT', key_spec='SYMMETRIC_DEFAULT')

