import json
import boto3
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
eks_client = boto3.client('eks')
dynamodb = boto3.resource('dynamodb')

# Configuration constants
CLUSTER_NAME = 'sas-6881323-eks'
REGION = 'sa-east-1'
LOGS_TABLE_NAME = 'eks-scaling-logs'
CONFIG_TABLE_NAME = 'eks-scaling-config'

# Node groups configuration
SMALL_NODEGROUP = 'default-20250319191255393900000026'  # m5.xlarge
BIG_NODEGROUP = 'new-m5a4xlarge-v4'  # m5a.4xlarge

def lambda_handler(event, context):
    """
    Main Lambda handler for EKS node scaling automation with DynamoDB configuration
    
    Handles timezone-aware scaling based on configurable schedules stored in DynamoDB.
    Supports different scaling modes: sleep (small nodes), normal (1 big node), 
    and peak (multiple big nodes).
    """
    try:
        # Get current local time (timezone-aware)
        local_time = get_local_time()
        logger.info(f"Current local time: {local_time}")
        
        # Load configuration from DynamoDB
        config = load_scaling_config()
        logger.info(f"Configuration loaded successfully")
        
        # Determine scaling action based on schedule and config
        scaling_action = determine_scaling_action(local_time, config)
        logger.info(f"Scaling action determined: {scaling_action['type']}")
        
        # Execute scaling operations
        result = execute_scaling(scaling_action, local_time)
        
        # Log execution results to DynamoDB
        log_scaling_action(scaling_action, result, local_time)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Scaling completed successfully',
                'action': scaling_action,
                'timestamp': local_time.isoformat(),
                'result': result,
                'config_version': config.get('version', '1.0')
            })
        }
        
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        }

def load_scaling_config() -> Dict[str, Any]:
    """
    Load scaling configuration from DynamoDB
    
    Returns the active configuration or falls back to defaults if unavailable.
    Configuration includes schedules, node limits, and operational parameters.
    """
    try:
        config_table = dynamodb.Table(CONFIG_TABLE_NAME)
        
        response = config_table.get_item(
            Key={'config_id': 'active'}
        )
        
        if 'Item' in response:
            config = response['Item']
            logger.info("Configuration loaded from DynamoDB")
            return config
        else:
            logger.warning("No configuration found in DynamoDB, using defaults")
            return get_default_config()
            
    except Exception as e:
        logger.error(f"Error loading configuration from DynamoDB: {str(e)}")
        logger.info("Using default configuration")
        return get_default_config()

def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration when DynamoDB config is unavailable
    
    Provides fallback configuration with standard schedules and limits.
    """
    return {
        'config_id': 'active',
        'cluster_name': CLUSTER_NAME,
        'small_nodegroup': SMALL_NODEGROUP,
        'big_nodegroup': BIG_NODEGROUP,
        'schedules': {
            'sleep_time': {
                'start_hour': 1,
                'start_minute': 0,
                'end_hour': 6,
                'end_minute': 30,
                'small_nodes': 1,
                'big_nodes': 0,
                'description': 'Sleep time - small nodegroup'
            },
            'peak_time': {
                'start_hour': 6,
                'start_minute': 30,
                'end_hour': 11,
                'end_minute': 30,
                'weekday': 1,  # Tuesday
                'small_nodes': 0,
                'big_nodes': 3,
                'description': 'Peak time - multiple big nodes'
            },
            'normal_operation': {
                'small_nodes': 0,
                'big_nodes': 1,
                'description': 'Normal operation - single big node'
            }
        },
        'nodegroup_limits': {
            'small_nodegroup': {
                'min_size': 0,
                'max_size': 1
            },
            'big_nodegroup': {
                'min_size': 0,
                'max_size': 3
            }
        },
        'enabled': True,
        'last_updated': datetime.now().isoformat(),
        'version': '1.0'
    }

def get_local_time():
    """
    Get current time in local timezone (UTC-3)
    
    Handles timezone conversion for accurate schedule matching.
    """
    utc_now = datetime.now(timezone.utc)
    local_timezone = timezone(timedelta(hours=-3))
    return utc_now.astimezone(local_timezone)

def determine_scaling_action(local_time: datetime, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Determine scaling action based on local time and configuration
    
    Implements business logic for different time periods:
    - Sleep time: Use small nodes for cost optimization
    - Peak time: Use multiple big nodes for performance (specific days)
    - Normal time: Use single big node for standard operations
    """
    if not config.get('enabled', True):
        return {
            'type': 'DISABLED',
            'description': 'Scaling is disabled in configuration',
            'small_nodegroup': {'desired': 0, 'min': 0, 'max': 1},
            'big_nodegroup': {'desired': 1, 'min': 1, 'max': 3}
        }
    
    hour = local_time.hour
    minute = local_time.minute
    weekday = local_time.weekday()  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    
    current_time_minutes = hour * 60 + minute
    schedules = config.get('schedules', {})
    limits = config.get('nodegroup_limits', {})
    
    # Check sleep time period
    sleep_config = schedules.get('sleep_time', {})
    sleep_start = sleep_config.get('start_hour', 1) * 60 + sleep_config.get('start_minute', 0)
    sleep_end = sleep_config.get('end_hour', 6) * 60 + sleep_config.get('end_minute', 30)
    
    if sleep_start <= current_time_minutes < sleep_end:
        return create_scaling_action(
            'S1', sleep_config, limits,
            sleep_config.get('description', 'Sleep time - small nodegroup')
        )
    
    # Check peak time period
    peak_config = schedules.get('peak_time', {})
    peak_start = peak_config.get('start_hour', 6) * 60 + peak_config.get('start_minute', 30)
    peak_end = peak_config.get('end_hour', 11) * 60 + peak_config.get('end_minute', 30)
    
    if (weekday == peak_config.get('weekday', 1) and 
        peak_start <= current_time_minutes < peak_end):
        return create_scaling_action(
            'B3', peak_config, limits,
            peak_config.get('description', 'Peak time - multiple big nodes')
        )
    
    # Check morning period (non-peak days)
    if peak_start <= current_time_minutes < peak_end:
        return create_scaling_action(
            'B1', schedules.get('normal_operation', {}), limits,
            'Morning normal operation - single big node'
        )
    
    # Default to normal operation
    normal_config = schedules.get('normal_operation', {})
    return create_scaling_action(
        'B1', normal_config, limits,
        normal_config.get('description', 'Normal operation - single big node')
    )

def create_scaling_action(action_type: str, schedule_config: Dict, limits: Dict, description: str) -> Dict[str, Any]:
    """
    Create scaling action configuration from schedule and limits
    
    Ensures desired node counts are within configured limits and
    sets appropriate minimum values based on desired counts.
    """
    small_limits = limits.get('small_nodegroup', {'min_size': 0, 'max_size': 1})
    big_limits = limits.get('big_nodegroup', {'min_size': 0, 'max_size': 3})
    
    small_desired = schedule_config.get('small_nodes', 0)
    big_desired = schedule_config.get('big_nodes', 1)
    
    # Set minimum values based on desired counts
    small_min = small_limits.get('min_size', 0) if small_desired > 0 else 0
    big_min = big_limits.get('min_size', 0) if big_desired > 0 else 0
    
    return {
        'type': action_type,
        'description': description,
        'small_nodegroup': {
            'desired': small_desired,
            'min': small_min,
            'max': small_limits.get('max_size', 1)
        },
        'big_nodegroup': {
            'desired': big_desired,
            'min': big_min,
            'max': big_limits.get('max_size', 3)
        }
    }

def execute_scaling(scaling_action: Dict[str, Any], local_time: datetime) -> Dict[str, Any]:
    """
    Execute scaling operations on EKS node groups
    
    Updates both small and big node groups according to the scaling action.
    Returns execution results for logging and monitoring.
    """
    results = {}
    
    try:
        # Scale small nodegroup
        small_config = scaling_action['small_nodegroup']
        small_result = update_nodegroup_scaling(
            SMALL_NODEGROUP, 
            small_config['desired'], 
            small_config['min'], 
            small_config['max']
        )
        results['small_nodegroup'] = small_result
        
        # Scale big nodegroup
        big_config = scaling_action['big_nodegroup']
        big_result = update_nodegroup_scaling(
            BIG_NODEGROUP, 
            big_config['desired'], 
            big_config['min'], 
            big_config['max']
        )
        results['big_nodegroup'] = big_result
        
        logger.info(f"Scaling operations completed")
        return results
        
    except Exception as e:
        logger.error(f"Error executing scaling operations: {str(e)}")
        raise

def update_nodegroup_scaling(nodegroup_name: str, desired: int, min_size: int, max_size: int) -> Dict[str, Any]:
    """
    Update individual nodegroup scaling configuration
    
    Calls EKS API to update nodegroup scaling parameters.
    Handles errors gracefully and returns structured results.
    """
    try:
        response = eks_client.update_nodegroup_config(
            clusterName=CLUSTER_NAME,
            nodegroupName=nodegroup_name,
            scalingConfig={
                'minSize': min_size,
                'maxSize': max_size,
                'desiredSize': desired
            }
        )
        
        return {
            'status': 'success',
            'update_id': response['update']['id'],
            'nodegroup': nodegroup_name,
            'scaling': {
                'desired': desired,
                'min': min_size,
                'max': max_size
            }
        }
        
    except Exception as e:
        logger.error(f"Error updating nodegroup {nodegroup_name}: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'nodegroup': nodegroup_name
        }

def log_scaling_action(scaling_action: Dict[str, Any], result: Dict[str, Any], local_time: datetime):
    """
    Log scaling action and results to DynamoDB
    
    Creates comprehensive audit trail for monitoring and troubleshooting.
    Includes execution results, configuration used, and timing information.
    """
    try:
        logs_table = dynamodb.Table(LOGS_TABLE_NAME)
        
        item = {
            'timestamp': local_time.isoformat(),
            'date': local_time.strftime('%Y-%m-%d'),
            'time': local_time.strftime('%H:%M:%S'),
            'weekday': local_time.strftime('%A'),
            'scaling_type': scaling_action['type'],
            'description': scaling_action['description'],
            'small_nodegroup_config': scaling_action['small_nodegroup'],
            'big_nodegroup_config': scaling_action['big_nodegroup'],
            'execution_result': result,
            'cluster_name': CLUSTER_NAME,
            'region': REGION
        }
        
        logs_table.put_item(Item=item)
        logger.info(f"Scaling action logged: {scaling_action['type']}")
        
    except Exception as e:
        logger.error(f"Error logging to DynamoDB: {str(e)}")
        # Don't raise exception to avoid failing the main scaling operation
