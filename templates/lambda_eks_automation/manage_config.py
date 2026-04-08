#!/usr/bin/env python3
"""
Interactive configuration management for EKS scaling
"""

import boto3
import json
from datetime import datetime
from setup_config import (
    load_configuration, save_configuration, display_configuration,
    update_schedule, enable_disable_scaling, CONFIG_TABLE_NAME, REGION
)

def show_menu():
    """Show the configuration management menu"""
    print("\n🔧 EKS Scaling Configuration Manager")
    print("=" * 50)
    print("1. View current configuration")
    print("2. Enable/Disable scaling")
    print("3. Update Tuesday peak hours")
    print("4. Update Tuesday peak node count")
    print("5. Update sleep time hours")
    print("6. Update normal operation node count")
    print("7. Update node limits")
    print("8. Export configuration to JSON")
    print("9. Import configuration from JSON")
    print("0. Exit")
    print("-" * 50)

def view_configuration():
    """View current configuration"""
    config = load_configuration()
    if config:
        display_configuration(config)
    else:
        print("❌ No configuration found. Run setup_config.py first.")

def toggle_scaling():
    """Enable or disable scaling"""
    config = load_configuration()
    if not config:
        print("❌ No configuration found")
        return
    
    current_status = config.get('enabled', True)
    print(f"Current status: {'Enabled' if current_status else 'Disabled'}")
    
    action = input("Enable (e) or Disable (d) scaling? ").lower()
    
    if action == 'e':
        enable_disable_scaling(True)
        print("✅ Scaling enabled")
    elif action == 'd':
        enable_disable_scaling(False)
        print("✅ Scaling disabled")
    else:
        print("❌ Invalid option")

def update_tuesday_peak_hours():
    """Update Tuesday peak hours"""
    print("🔄 Update Tuesday Peak Hours")
    print("Current format: HH:MM (24-hour format)")
    
    try:
        start_time = input("Enter start time (e.g., 06:30): ")
        end_time = input("Enter end time (e.g., 11:30): ")
        
        start_hour, start_minute = map(int, start_time.split(':'))
        end_hour, end_minute = map(int, end_time.split(':'))
        
        if update_schedule('tuesday_peak', 
                          start_hour=start_hour, start_minute=start_minute,
                          end_hour=end_hour, end_minute=end_minute):
            print(f"✅ Tuesday peak hours updated to {start_time} - {end_time}")
        else:
            print("❌ Failed to update")
            
    except ValueError:
        print("❌ Invalid time format. Use HH:MM")

def update_tuesday_peak_nodes():
    """Update Tuesday peak node count"""
    print("🔄 Update Tuesday Peak Node Count")
    
    try:
        big_nodes = int(input("Enter number of big nodes for Tuesday peak (current: 3): "))
        small_nodes = int(input("Enter number of small nodes for Tuesday peak (current: 0): "))
        
        if update_schedule('tuesday_peak', big_nodes=big_nodes, small_nodes=small_nodes):
            print(f"✅ Tuesday peak nodes updated: {big_nodes} big, {small_nodes} small")
        else:
            print("❌ Failed to update")
            
    except ValueError:
        print("❌ Invalid number format")

def update_sleep_hours():
    """Update sleep time hours"""
    print("🔄 Update Sleep Time Hours")
    
    try:
        start_time = input("Enter sleep start time (e.g., 01:00): ")
        end_time = input("Enter sleep end time (e.g., 06:30): ")
        
        start_hour, start_minute = map(int, start_time.split(':'))
        end_hour, end_minute = map(int, end_time.split(':'))
        
        if update_schedule('sleep_time',
                          start_hour=start_hour, start_minute=start_minute,
                          end_hour=end_hour, end_minute=end_minute):
            print(f"✅ Sleep hours updated to {start_time} - {end_time}")
        else:
            print("❌ Failed to update")
            
    except ValueError:
        print("❌ Invalid time format. Use HH:MM")

def update_normal_nodes():
    """Update normal operation node count"""
    print("🔄 Update Normal Operation Node Count")
    
    try:
        big_nodes = int(input("Enter number of big nodes for normal operation (current: 1): "))
        small_nodes = int(input("Enter number of small nodes for normal operation (current: 0): "))
        
        if update_schedule('normal_operation', big_nodes=big_nodes, small_nodes=small_nodes):
            print(f"✅ Normal operation nodes updated: {big_nodes} big, {small_nodes} small")
        else:
            print("❌ Failed to update")
            
    except ValueError:
        print("❌ Invalid number format")

def update_node_limits():
    """Update node group limits"""
    print("🔄 Update Node Group Limits")
    
    config = load_configuration()
    if not config:
        print("❌ No configuration found")
        return
    
    try:
        print("Small nodegroup limits:")
        small_min = int(input("  Min size (current: 0): "))
        small_max = int(input("  Max size (current: 1): "))
        
        print("Big nodegroup limits:")
        big_min = int(input("  Min size (current: 0): "))
        big_max = int(input("  Max size (current: 3): "))
        
        config['nodegroup_limits'] = {
            'small_nodegroup': {'min_size': small_min, 'max_size': small_max},
            'big_nodegroup': {'min_size': big_min, 'max_size': big_max}
        }
        config['last_updated'] = datetime.now().isoformat()
        
        if save_configuration(config):
            print("✅ Node limits updated successfully")
        else:
            print("❌ Failed to update")
            
    except ValueError:
        print("❌ Invalid number format")

def export_configuration():
    """Export configuration to JSON file"""
    config = load_configuration()
    if not config:
        print("❌ No configuration found")
        return
    
    filename = f"eks_scaling_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2, default=str)
        
        print(f"✅ Configuration exported to {filename}")
        
    except Exception as e:
        print(f"❌ Export failed: {str(e)}")

def import_configuration():
    """Import configuration from JSON file"""
    filename = input("Enter JSON filename to import: ")
    
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
        
        # Validate required fields
        required_fields = ['config_id', 'schedules', 'nodegroup_limits']
        for field in required_fields:
            if field not in config:
                print(f"❌ Invalid configuration: missing '{field}'")
                return
        
        config['last_updated'] = datetime.now().isoformat()
        config['imported_at'] = datetime.now().isoformat()
        
        if save_configuration(config):
            print("✅ Configuration imported successfully")
            display_configuration(config)
        else:
            print("❌ Failed to save imported configuration")
            
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found")
    except json.JSONDecodeError:
        print("❌ Invalid JSON format")
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")

def main():
    """Main configuration management interface"""
    print("🚀 EKS Scaling Configuration Manager")
    print(f"DynamoDB Table: {CONFIG_TABLE_NAME}")
    print(f"Region: {REGION}")
    
    while True:
        show_menu()
        
        try:
            choice = input("Select option (0-9): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            elif choice == '1':
                view_configuration()
            elif choice == '2':
                toggle_scaling()
            elif choice == '3':
                update_tuesday_peak_hours()
            elif choice == '4':
                update_tuesday_peak_nodes()
            elif choice == '5':
                update_sleep_hours()
            elif choice == '6':
                update_normal_nodes()
            elif choice == '7':
                update_node_limits()
            elif choice == '8':
                export_configuration()
            elif choice == '9':
                import_configuration()
            else:
                print("❌ Invalid option. Please select 0-9.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
