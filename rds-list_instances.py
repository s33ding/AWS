import boto3
import pandas as pd
import sys

def list_rds_instances_as_df(instance_id=None, region='us-east-1'):
    # Create an RDS client
    rds = boto3.client('rds', region_name=region)

    try:
        if instance_id:
            # Describe a specific instance
            response = rds.describe_db_instances(DBInstanceIdentifier=instance_id)
        else:
            # Describe all instances
            response = rds.describe_db_instances()

        instances = response.get('DBInstances', [])
        if not instances:
            print("No RDS instances found.")
            return pd.DataFrame()

        # Extract relevant data
        data = []
        for db in instances:
            data.append({
                'DBInstanceIdentifier': db['DBInstanceIdentifier'],
                'Engine': db['Engine'],
                'Status': db['DBInstanceStatus'],
                'Endpoint': db['Endpoint']['Address'],
                'InstanceClass': db['DBInstanceClass'],
                'Region': region
            })

        # Create DataFrame
        df = pd.DataFrame(data)
        print(df)
        return df

    except Exception as e:
        print("Error retrieving RDS instances:", e)
        return pd.DataFrame()

# Run the function
if __name__ == "__main__":
    instance_id = sys.argv[1] if len(sys.argv) > 1 else None
    list_rds_instances_as_df(instance_id)

