# Function to invoke another Lambda function
def invoke_lamb(my_payload, lambda_name, invocation_type):
  client = boto3.client("lambda")
  response = client.invoke(
      FunctionName = lambda_name,
      InvocationType = invocation_type, # best options: RequestResponse or Event
      Payload = json.dumps(my_payload))
  return response
  
def extract_response_value(lambda_response):
    response_body = json.loads(lambda_response['Payload'].read().decode())
    data_cleaned = json.loads(response_body['body'])
    return data_cleaned
def lambda_handler(event, context):
    dct = json.loads(event['body'])

    lambda_response = invoke_lamb(
            my_payload = dct,
            lambda_name = 'arn:aws:lambda:us-east-1:xxxxxxxxxxxxxxxx',
            invocation_type = "RequestResponse")
        
    response= extract_response_value(lambda_response)
