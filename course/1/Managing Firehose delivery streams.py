# Import boto3 and create boto3 Firehose client
import boto3
firehose = boto3.client('firehose', 
    aws_access_key_id=AWS_KEY_ID, aws_secret_access_key=AWS_SECRET, 
    region_name='us-east-1', endpoint_url=endpoints['FIREHOSE'])

# Get list of delivery streams
response = firehose.list_delivery_streams()

# Iterate over the response contents and delete every stream
for stream_name in response['DeliveryStreamNames']:
    firehose.delete_delivery_stream(DeliveryStreamName=stream_name)
    print(f"Deleted stream: {stream_name}")

# Print list of delivery streams
print(firehose.list_delivery_streams())