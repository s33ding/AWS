import boto3
from datetime import datetime, timedelta
import calendar

def get_s3_cost(d=0, service='Amazon Simple Storage Service', granularity='DAILY', usage_filter=None):
    """
    Get S3 cost for a specific period.
    
    Args:
        d (int): Day offset from today. 0=today, -1=yesterday, etc.
        service (str): AWS service name, defaults to S3
        granularity (str): DAILY or MONTHLY
        usage_filter (str): Filter by usage type (e.g., 'Requests')
    
    Returns:
        float: Total cost for the specified service and period
    """
    ce = boto3.client('ce')
    
    if granularity == 'MONTHLY':
        # Get the target month
        target_date = datetime.now() + timedelta(days=d*30)  # Approximate month offset
        year = target_date.year
        month = target_date.month
        
        # Get first and last day of the month
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])
        
        start_time = first_day.strftime('%Y-%m-%d')
        end_time = (last_day + timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        # Daily - single day
        target_date = datetime.now() + timedelta(days=d)
        start_time = target_date.strftime('%Y-%m-%d')
        end_time = (target_date + timedelta(days=1)).strftime('%Y-%m-%d')
    
    group_by = [{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    if usage_filter:
        group_by.append({'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'})
    
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_time,
            'End': end_time
        },
        Granularity=granularity,
        Metrics=['BlendedCost'],
        GroupBy=group_by
    )
    
    s3_cost = 0.0
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            if service in group['Keys'][0]:
                if usage_filter:
                    # Check if usage type contains filter string
                    if len(group['Keys']) > 1 and usage_filter in group['Keys'][1]:
                        s3_cost += float(group['Metrics']['BlendedCost']['Amount'])
                else:
                    s3_cost += float(group['Metrics']['BlendedCost']['Amount'])
    
    return round(s3_cost, 2)
