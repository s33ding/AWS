from shared_func.kms_func import *
from shared_func.argv_parser import *

lst = list_kms_keys()

for dct in lst:
    print("--------------------------------------")
    for k,v in dct.items():
        print(k,v)

