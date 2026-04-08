#!/usr/bin/env python3
import configparser
import os
import shutil
import boto3
import sys

def get_default_endpoint_url():
    config_path = os.path.expanduser('~/.aws/config')
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    return config.get('default', 'endpoint_url', fallback=None)

def get_whoami():
    try:
        session = boto3.Session()
        endpoint_url = get_default_endpoint_url()
        if endpoint_url:
            s3 = session.client('s3', endpoint_url=endpoint_url)
            buckets = s3.list_buckets()
            return {
                'endpoint': endpoint_url,
                'buckets': len(buckets.get('Buckets', [])),
                'type': 's3-compatible'
            }
        else:
            sts_client = session.client('sts')
            identity = sts_client.get_caller_identity()
            region = session.region_name or "us-east-1"
            return {
                'account': identity['Account'],
                'user_id': identity['UserId'],
                'arn': identity['Arn'],
                'region': region,
                'type': 'aws'
            }
    except Exception as e:
        return {'error': str(e)}

def print_banner():
    print("=" * 60)
    print("🔄 AWS Profile Switcher")
    print("=" * 60)

def mask_sensitive(value, show_last=4):
    if not value or len(value) <= show_last:
        return '*' * len(value)
    return '*' * (len(value) - show_last) + value[-show_last:]

def print_current_identity(info):
    if 'error' in info:
        print(f"❌ Error getting identity: {info['error']}")
        return
    
    print(f"✅ Current Identity:")
    if info.get('type') == 's3-compatible':
        print(f"   Endpoint: {info['endpoint']}")
        print(f"   Buckets:  {info['buckets']}")
    else:
        print(f"   Account: {info['account']}")
        print(f"   User:    {info['user_id']}")
        print(f"   ARN:     {info['arn']}")
        print(f"   Region:  {info['region']}")

def get_profiles():
    creds_path = os.path.expanduser('~/.aws/credentials')
    if not os.path.exists(creds_path):
        print("❌ AWS credentials file not found")
        return {}
    
    config = configparser.ConfigParser()
    config.read(creds_path)
    
    profiles = {}
    for section in config.sections():
        if section != 'default':
            profile_data = {}
            for key, value in config[section].items():
                if 'key' in key.lower() or 'token' in key.lower():
                    profile_data[key] = value
                else:
                    profile_data[key] = value
            profiles[section] = profile_data
    return profiles

def show_menu(profiles):
    print("\n" + "─" * 40)
    print("📋 Available Profiles:")
    for i, profile in enumerate(profiles.keys(), 1):
        print(f"   {i}. {profile}")
    print("─" * 40)
    print("🌎 Regions: 'us', 'sa'")
    print("─" * 40)
    return input("Select: ")

def change_region(region_code):
    config_path = os.path.expanduser('~/.aws/config')
    
    region_map = {
        'us': 'us-east-1',
        'sa': 'sa-east-1'
    }
    
    new_region = region_map.get(region_code.lower())
    if not new_region:
        return False
    
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    
    if 'default' not in config:
        config.add_section('default')
    
    config.set('default', 'region', new_region)
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        config.write(f)
    
    print(f"\n🌎 Region changed to: {new_region}")
    return True

def update_default_profile(selected_profile, profiles):
    creds_path = os.path.expanduser('~/.aws/credentials')
    config_path = os.path.expanduser('~/.aws/config')
    backup_path = f"{creds_path}.backup"
    
    shutil.copy2(creds_path, backup_path)
    
    config = configparser.ConfigParser()
    config.read(creds_path)
    
    if 'default' in config:
        config.remove_section('default')
    
    config.add_section('default')
    for key, value in profiles[selected_profile].items():
        config.set('default', key, value)
    
    with open(creds_path, 'w') as f:
        config.write(f)
    
    # Sync endpoint_url in config
    aws_config = configparser.ConfigParser()
    if os.path.exists(config_path):
        aws_config.read(config_path)
    if 'default' not in aws_config:
        aws_config.add_section('default')
    
    profile_section = f'profile {selected_profile}'
    endpoint = aws_config.get(profile_section, 'endpoint_url', fallback=None)
    if endpoint:
        aws_config.set('default', 'endpoint_url', endpoint)
    elif aws_config.has_option('default', 'endpoint_url'):
        aws_config.remove_option('default', 'endpoint_url')
    
    with open(config_path, 'w') as f:
        aws_config.write(f)
    
    print(f"\n🔄 Switched to profile: {selected_profile}")

def parse_input(choice, profiles):
    import re
    
    # Check for combined input like "1us", "us1", "sa2"
    match = re.match(r'(\d+)(us|sa)|^(us|sa)(\d+)$', choice.lower())
    if match:
        if match.group(1):  # Format: 1us, 2sa
            profile_idx = int(match.group(1)) - 1
            region = match.group(2)
        else:  # Format: us1, sa2
            region = match.group(3)
            profile_idx = int(match.group(4)) - 1
        
        profile_names = list(profiles.keys())
        if 0 <= profile_idx < len(profile_names):
            return 'combined', profile_names[profile_idx], region
    
    # Check for region only
    if choice.lower() in ['us', 'sa']:
        return 'region', None, choice.lower()
    
    # Check for profile number only
    try:
        idx = int(choice) - 1
        profile_names = list(profiles.keys())
        if 0 <= idx < len(profile_names):
            return 'profile', profile_names[idx], None
    except ValueError:
        pass
    
    return 'invalid', None, None

def main():
    print_banner()
    
    # Show current identity
    current_info = get_whoami()
    print_current_identity(current_info)
    
    profiles = get_profiles()
    if not profiles:
        return
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if len(sys.argv) == 3:
            # Two arguments: region and profile-name in any order
            args = sys.argv[1:3]
            region = next((arg for arg in args if arg.lower() in ['us', 'sa']), None)
            profile_name = next((arg for arg in args if arg.lower() not in ['us', 'sa']), None)
            
            if region and profile_name and profile_name in profiles:
                update_default_profile(profile_name, profiles)
                change_region(region)
                print("\n" + "─" * 40)
                new_info = get_whoami()
                print_current_identity(new_info)
                return
            else:
                print("❌ Invalid profile name or region")
                return
        else:
            choice = sys.argv[1]
    else:
        choice = show_menu(profiles)
    
    action, profile, region = parse_input(choice, profiles)
    
    if action == 'combined':
        update_default_profile(profile, profiles)
        change_region(region)
        print("\n" + "─" * 40)
        new_info = get_whoami()
        print_current_identity(new_info)
    elif action == 'region':
        if change_region(region):
            print("\n" + "─" * 40)
            new_info = get_whoami()
            print_current_identity(new_info)
    elif action == 'profile':
        update_default_profile(profile, profiles)
        print("\n" + "─" * 40)
        new_info = get_whoami()
        print_current_identity(new_info)
    else:
        print("❌ Invalid input")

if __name__ == "__main__":
    main()
