#!/usr/bin/env python3
import configparser
import os
import shutil
import boto3

def get_whoami():
    try:
        session = boto3.Session()
        sts_client = session.client('sts')
        identity = sts_client.get_caller_identity()
        region = session.region_name or "us-east-1"
        
        return {
            'account': identity['Account'],
            'user_id': identity['UserId'],
            'arn': identity['Arn'],
            'region': region
        }
    except Exception as e:
        return {'error': str(e)}

def print_banner():
    print("=" * 60)
    print("🔄 AWS Profile Switcher")
    print("=" * 60)

def print_current_identity(info):
    if 'error' in info:
        print(f"❌ Error getting identity: {info['error']}")
        return
    
    print(f"✅ Current Identity:")
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
    return {section: dict(config[section]) for section in config.sections() if section != 'default'}

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
    
def main():
    print_banner()
    
    # Show current identity
    current_info = get_whoami()
    print_current_identity(current_info)
    
    profiles = get_profiles()
    if not profiles:
        return
    
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
