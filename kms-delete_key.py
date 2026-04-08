from shared_func.kms_func import *
from shared_func.argv_parser import *

key_id = input('key_id:')

delete_kms_key(key_id)


