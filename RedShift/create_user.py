import warnings
import json
import redshift_connector

warnings.filterwarnings("ignore")

with open(os.environ["RedShift_CRED"], 'r') as file:
    db  = json.load(file)

conn = redshift_connector.connect(host = db['host'],database = db['database'], user= db['user'], password= db['password'])
redshift_connector.Cursor = conn.cursor()

user_name = input("USER_NAME: ")
user_password = input("PASSWORD: ")

cursor: redshift_connector.Cursor = conn.cursor()
cmd = f"create user {user_name} password '{user_password}';"
res = cursor.execute(cmd)
