def invoke_lamb(name, arg = "", type = "Event"):
    region = "us-east-1"
    account = "?"
    client = boto3.client("lambda")
    
    if type == "Event":
        client.invoke(
        FunctionName = f"arn:aws:lambda:{region}:{account}:function:{name}",
        InvocationType = 'Event', 
        Payload = json.dumps(arg))
    
    else: 
        response = client.invoke(
        FunctionName = f"arn:aws:lambda:{region}:{account}:function:{name}",
        InvocationType = 'RequestResponse', 
        Payload = json.dumps(arg))
        return response