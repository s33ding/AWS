Explanation of Session, Client, and Resource in Boto3

Session represents a connection to the AWS services. When you create a Session object, it automatically creates a default boto3 Client and Resource object. You can use the Client object to call AWS APIs directly, and you can use the Resource object to interact with AWS resources (like DynamoDB tables, S3 buckets, etc.) at a higher level of abstraction.

Client represents a low-level AWS service client. You use the Client object to call AWS APIs directly. For example, if you want to call the put_item method on a DynamoDB table, you would create a DynamoDB client and call put_item on that client.

Resource represents a higher-level AWS service resource. You use the Resource object to interact with AWS resources at a higher level of abstraction. For example, if you want to interact with a DynamoDB table, you would create a DynamoDB resource, retrieve the table object using the Table method on that resource, and call methods on the table object (like put_item, get_item, etc.) to interact with the table.

The reason it can be confusing is that boto3 provides different levels of abstraction for interacting with AWS services. Depending on your use case, you may want to use a higher-level Resource object or a lower-level Client object. It's important to understand the differences between these objects and when to use each one.
