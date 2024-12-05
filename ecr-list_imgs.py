import sys
from shared_func.ecr_func import *
import json
import os
import config


res = list_ecr_images(repository_name=config.repo_name)

for img in res:
	print(img) 

