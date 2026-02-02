#!/usr/bin/env python3
import os
import sys

if len(sys.argv) != 2:
    print("Usage: python3 s3-lifecycle.py <bucket-name>")
    sys.exit(1)

bucket = sys.argv[1]
cmd = f'aws s3api put-bucket-lifecycle-configuration --bucket {bucket} --lifecycle-configuration \'{{"Rules":[{{"Expiration":{{"Days":1}},"Filter":{{}},"ID":"DeleteAfter24Hours","Status":"Enabled"}}]}}\''

os.system(cmd)
