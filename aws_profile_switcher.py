#!/usr/bin/env python3
import configparser
import os
import shutil

def get_profiles():
    creds_path = os.path.expanduser('~/.aws/credentials')
    if not os.path.exists(creds_path):
        print("AWS credentials file not found")
        return {}
    
    config = configparser.ConfigParser()
    config.read(creds_path)
    return {section: dict(config[section]) for section in config.sections() if section != 'default'}

def get_current_default():
    creds_path = os.path.expanduser('~/.aws/credentials')
    config_path = os.path.expanduser('~/.aws/config')
    
    config = configparser.ConfigParser()
    config.read(creds_path)
    
    region = "us-east-1"
    if os.path.exists(config_path):
        aws_config = configparser.ConfigParser()
        aws_config.read(config_path)
        if 'default' in aws_config:
            region = aws_config['default'].get('region', region)
    
    if 'default' in config:
        access_key = config['default'].get('aws_access_key_id', 'Unknown')
        # Show only last 4 chars for security
        masked_key = f"***{access_key[-4:]}" if len(access_key) > 4 else "***"
        return f"Current default: {masked_key}, region: {region}"
    return f"No default profile set, region: {region}"

def show_menu(profiles):
    print(f"\n{get_current_default()}")
    print("\nAvailable AWS Profiles:")
    for i, profile in enumerate(profiles.keys(), 1):
        print(f"{i}. {profile}")
    return input("\nSelect profile number (or 'q' to quit): ")

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
    
    print(f"Default profile updated to: {selected_profile}")

def main():
    profiles = get_profiles()
    if not profiles:
        return
    
    while True:
        choice = show_menu(profiles)
        
        if choice.lower() == 'q':
            break
        
        try:
            idx = int(choice) - 1
            profile_names = list(profiles.keys())
            if 0 <= idx < len(profile_names):
                selected = profile_names[idx]
                update_default_profile(selected, profiles)
                break
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")

if __name__ == "__main__":
    main()
