import sys
from shared_func.ecr_func import *
import json
import os
import config

input_func = lambda: sys.argv[1] if len(sys.argv) > 1 else config.repo_name

repo_name = input_func()

res = list_ecr_images(repo_name)

for img in res:
	print(img) 

