import boto3
import pandas as pd
from shared_func.ec2_func import *


df = list_ec2_instances()
