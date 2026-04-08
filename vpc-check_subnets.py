#!/usr/bin/env python3
import boto3

def check_vpc_subnets():
    ec2 = boto3.client('ec2', region_name='us-east-1')
    
    # Get all VPCs
    vpcs = ec2.describe_vpcs()
    
    for vpc in vpcs['Vpcs']:
        vpc_id = vpc['VpcId']
        cidr_block = vpc['CidrBlock']
        is_default = vpc.get('IsDefault', False)
        vpc_name = next((tag['Value'] for tag in vpc.get('Tags', []) if tag['Key'] == 'Name'), 'No Name')
        
        print(f"VPC: {vpc_name} ({vpc_id})")
        print(f"CIDR Block: {cidr_block}")
        print(f"Default VPC: {is_default}")
        
        # Get subnets for this VPC
        subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        
        if subnets['Subnets']:
            print("Subnets:")
            for subnet in subnets['Subnets']:
                subnet_id = subnet['SubnetId']
                subnet_cidr = subnet['CidrBlock']
                az = subnet['AvailabilityZone']
                subnet_name = next((tag['Value'] for tag in subnet.get('Tags', []) if tag['Key'] == 'Name'), 'No Name')
                print(f"  - {subnet_name} ({subnet_id}) | {subnet_cidr} | {az}")
        else:
            print("  No subnets found")
        
        print("-" * 50)

if __name__ == "__main__":
    check_vpc_subnets()
