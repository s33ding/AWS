import boto3
import sys

def control_rds_instance(instance_id, control_flag, region='us-east-1'):
    rds = boto3.client('rds', region_name=region)

    try:
        if control_flag == 1:
            print(f"Starting RDS instance: {instance_id}")
            response = rds.start_db_instance(DBInstanceIdentifier=instance_id)
        elif control_flag == 0:
            print(f"Stopping RDS instance: {instance_id}")
            response = rds.stop_db_instance(DBInstanceIdentifier=instance_id)
        else:
            print("Invalid control_flag. Use 1 to start and 0 to stop.")
            return

        status = response['DBInstance']['DBInstanceStatus']
        print(f"Action initiated. Current status: {status}")

    except Exception as e:
        print(f"Error controlling RDS instance '{instance_id}':", e)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <instance_id> <control_flag (1=start, 0=stop)>")
        sys.exit(1)

    instance_id = sys.argv[1]
    try:
        control_flag = int(sys.argv[2])
    except ValueError:
        print("Control flag must be an integer: 1 to start, 0 to stop")
        sys.exit(1)

    control_rds_instance(instance_id, control_flag)

