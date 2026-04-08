#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

ce = boto3.client('ce', region_name='us-east-1')
now = datetime.now()
today = now.strftime('%Y-%m-%d')

# Last 3 months - monthly breakdown
three_months_ago = (now - timedelta(days=90)).strftime('%Y-%m-%d')
r = ce.get_cost_and_usage(
    TimePeriod={'Start': three_months_ago, 'End': today},
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    Filter={'Dimensions': {'Key': 'RECORD_TYPE', 'Values': ['Credit']}}
)
print("Credits used - Last 3 months (by month):")
monthly_total = 0
for item in r['ResultsByTime']:
    credits = abs(float(item['Total']['UnblendedCost']['Amount']))
    monthly_total += credits
    print(f"  {item['TimePeriod']['Start']}: ${credits:.2f}")
print(f"Total: ${monthly_total:.2f}")

# Last 3 weeks - daily breakdown
three_weeks_ago = (now - timedelta(days=21)).strftime('%Y-%m-%d')
r = ce.get_cost_and_usage(
    TimePeriod={'Start': three_weeks_ago, 'End': today},
    Granularity='DAILY',
    Metrics=['UnblendedCost'],
    Filter={'Dimensions': {'Key': 'RECORD_TYPE', 'Values': ['Credit']}}
)
print("\nCredits used - Last 3 weeks (by day):")
daily_total = 0
for item in r['ResultsByTime']:
    credits = abs(float(item['Total']['UnblendedCost']['Amount']))
    daily_total += credits
    if credits > 0:
        print(f"  {item['TimePeriod']['Start']}: ${credits:.2f}")
print(f"Total: ${daily_total:.2f}")
