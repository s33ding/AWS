> To create a Firehose

1. create a user.
2. add permissions AmazonkinesesFirehoseFullAcess(create and manage Firehose stream).
3. Create firehose deliverole for alow the Firehouse to write in the S3 bucket. 

OBS:More informations is on the second video from the course.

> Create a Role

1. Go to IAM
2. Go to Roles
3. Create a Role w/ AWS Service as the entity type.
4. Bellow select the Kinesis as the service
5. Select Kinesis Firehose as the use case.
6. Grant S3FullAcess permission
7. Name it.

> create stream 

1. Go to roles in IAM -> firehoseDeliveryRole 
2. COPY the -> Role ARN to use BOTO3
3. 