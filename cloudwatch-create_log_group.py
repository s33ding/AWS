import os
import time
from shared_func.cloudwatch_func import create_log_group
from shared_func.argv_parser import get_input

log_group_name = get_input("log_group_name:")
resp = create_log_group(log_group_name)
print(resp)
