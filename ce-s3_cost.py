#!/usr/bin/env python3
import argparse
from shared_func.cost_explorer_func import get_s3_cost

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--d', type=int, help='Day granularity with day offset')
    parser.add_argument('--m', type=int, help='Month granularity with day offset')
    parser.add_argument('--api', action='store_true', help='Filter for S3 API Requests - Standard')
    args = parser.parse_args()
    
    usage_filter = 'Requests' if args.api else None
    
    if args.m is not None:
        cost = get_s3_cost(args.m, granularity='MONTHLY', usage_filter=usage_filter)
        period = 'month'
    else:
        d = args.d if args.d is not None else -1
        cost = get_s3_cost(d, granularity='DAILY', usage_filter=usage_filter)
        period = 'day'
    
    filter_type = 'Requests (all tiers)' if args.api else 'total'
    print(f"S3 {filter_type} cost ({period}): ${cost}")
