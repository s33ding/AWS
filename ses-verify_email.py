import sys
from shared_func.ses_func import *

# Define lambda function to set default user name if not provided as an argument
email = input("email:")

verify_email(email)
