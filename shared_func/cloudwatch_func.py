import boto3

def delete_log_group(log_group_name):
    # create a CloudWatch Logs client
    client = boto3.client('logs')

    # list all log streams within the log group
    response = client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy='LastEventTime',
        descending=True
    )
    log_streams = response.get('logStreams', [])

    # delete all log events within each log stream
    for log_stream in log_streams:
        client.delete_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream['logStreamName']
        )

    # delete the log group
    client.delete_log_group(logGroupName=log_group_name)

    # return the response
    return True


def create_log_stream(log_group_name, log_stream_name):
    # create a CloudWatch Logs client
    client = boto3.client('logs')

    # create a new log stream
    response = client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)

    # return the response
    return response

def create_log_group(log_group_name):
    # create a CloudWatch Logs client
    client = boto3.client('logs')

    # create the log group
    response = client.create_log_group(logGroupName=log_group_name)

    # print the response
    print(response)

    # return the response
    return response

def get_log_events(log_group_name, log_stream_name):
    # create a CloudWatch Logs client
    client = boto3.client('logs')

    # get the log events from the log stream
    response = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name
    )
    # return the log events
    return response['events']

def send_log_data(log_group_name, log_stream_name, log_data):
    # create a CloudWatch Logs client
    client = boto3.client('logs')

    # put log event to the new log stream
    log_event = {
        'timestamp': int(time.time() * 1000),
        'message': log_data
    }
