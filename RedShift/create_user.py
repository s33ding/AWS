import random
import warnings
import sys
import string
import json
import redshift_connector
import os

warnings.filterwarnings("ignore")

def random_case(s):
    res = random.choice([0,1])
    if res == 0:
        return s
    else: return s.lower()

def random_password(n):
    n = int(n)
    lst_letters = [random_case(x) for x in string.ascii_uppercase]
    lst_special_chars = "\/@".split()
    lst_digits = [str(x) for x in string.digits]
    lst = lst_letters + lst_digits + lst_special_chars + lst_special_chars
    return "".join([random.choice(lst) for x in range(n)])

with open(os.environ["REDSHIFT_CRED"], 'r') as file:
    db  = json.load(file)

#conn = redshift_connector.connect(host = db['host'],database = db['database'], user= db['user'], password= db['password'])
#redshift_connector.Cursor = conn.cursor()

new_user_name = sys.argv[1]
new_user_password = random_password(32)

#cursor: redshift_connector.Cursor = conn.cursor()
#cmd = f"create user {user_name} password '{user_password}';"
#res = cursor.execute(cmd)

cred = db
cred["user"] = new_user_name
cred["password"] = new_user_password

for info in ["iam_role_arn","tempdir"]:
    cred.pop(info)

with open(f"RedShift_CRED_{new_user_name.title()}.json", "w") as f:
        json.dump(cred,f,indent=4)
