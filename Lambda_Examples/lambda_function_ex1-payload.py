from mykit import s3_upload_obj
import json
import boto3



def lambda_handler(event, context):
    
    dct = json.loads(event['body'])
    
    res = s3_upload_obj(bucket_name='bucket-ex',
        file_name='x.json', 
        folder_name="folder-ex", 
        string=json.dumps(dct, indent=4))
  
    return {'statusCode': 200,'body': json.dumps("OK")}
