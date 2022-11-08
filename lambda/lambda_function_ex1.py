from mykit import s3_upload_obj
import json
import boto3



def lambda_handler(event, context):
    
    dct = json.loads(event['body'])
    

    res = s3_upload_obj(bucket_name='bucket-ex',
        file_name='x.json', 
        folder_name="folder-ex", 
        string=json.dumps(dct, indent=4))

 
    client = boto3.client("lambda")
  
    response = client.invoke(FunctionName = f"arn:aws:lambda:{region}:{account}:function:{name}",InvocationType = "Event") # InvocationTypes: RequestResponse | Event
    return {'statusCode': 200,'body': json.dumps("OK")}