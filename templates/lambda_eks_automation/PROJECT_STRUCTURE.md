# EKS Scaling Automation - Project Structure

## 📁 Core Files

```
eks-scaling-automation/
├── 🚀 DEPLOYMENT
│   ├── deploy.sh                    # One-click deployment script
│   ├── deploy_infrastructure.py     # AWS resource creation (boto3)
│   └── requirements.txt             # Python dependencies
│
├── ⚡ LAMBDA FUNCTION  
│   ├── lambda_function.py           # Main scaling logic
│   └── lambda_deployment.zip        # Deployment package (auto-generated)
│
├── 🔧 CONFIGURATION
│   ├── setup_config.py             # Initial configuration setup
│   ├── manage_config.py            # Interactive config management
│   └── update_cron_schedule.py     # Schedule management
│
├── 🧪 TESTING
│   ├── test_lambda.py              # Unit tests for scaling logic
│   ├── test_scale_up.py            # Scale-up functionality tests
│   ├── test_real_scaling.py        # Real AWS integration tests
│   ├── test_all_modes.py           # Comprehensive mode testing
│   └── manual_scale_test.py        # Manual testing utilities
│
├── 📊 MONITORING
│   ├── monitor.py                  # System status and health checks
│   └── demo_config_changes.py      # Configuration demo script
│
└── 📚 DOCUMENTATION
    ├── README.md                   # Complete project documentation
    ├── README_CLEAN.md             # Clean technical overview
    ├── PROJECT_STRUCTURE.md        # This file
    └── TEST_RESULTS.md             # Comprehensive test results
```

## 🎯 Key Components

### Core Lambda Function (`lambda_function.py`)
- **Timezone handling**: São Paulo time calculations
- **Configuration loading**: DynamoDB-driven parameters
- **Scaling logic**: Day/time-based node management
- **Error handling**: Comprehensive exception management
- **Logging**: Full audit trail to DynamoDB

### Infrastructure Deployment (`deploy_infrastructure.py`)
- **IAM roles**: Least-privilege security model
- **DynamoDB tables**: Configuration and logging storage
- **EventBridge rules**: Automated cron scheduling
- **Lambda function**: Code deployment and configuration
- **Permissions**: Cross-service access management

### Configuration System
- **Dynamic parameters**: No code deployment for changes
- **Schedule management**: Time-based scaling rules
- **Node limits**: Safety constraints and boundaries
- **Enable/disable**: System-wide control switches

### Testing Suite
- **Unit tests**: Logic validation and edge cases
- **Integration tests**: Real AWS service interaction
- **Performance tests**: Scaling time and reliability
- **Configuration tests**: Parameter validation

## 🔄 Workflow

### 1. Initial Setup
```bash
./deploy.sh                    # Deploy all AWS resources
python3 setup_config.py       # Initialize configuration
python3 test_lambda.py        # Validate deployment
```

### 2. Configuration Management
```bash
python3 manage_config.py      # Interactive configuration
# OR edit DynamoDB table directly via AWS Console
```

### 3. Monitoring & Maintenance
```bash
python3 monitor.py            # Check system health
aws logs tail /aws/lambda/eks-scaling-automation --follow
```

## 🏗️ AWS Resources Created

### Lambda Function
- **Name**: `eks-scaling-automation`
- **Runtime**: Python 3.11
- **Memory**: 256 MB
- **Timeout**: 5 minutes
- **Environment**: Production-ready configuration

### DynamoDB Tables
- **eks-scaling-config**: Configuration parameters
- **eks-scaling-logs**: Execution audit trail

### EventBridge Rules
- **eks-scaling-sleep-period**: 01:00 daily (sleep mode)
- **eks-scaling-morning-period**: 06:30 daily (morning scaling)
- **eks-scaling-afternoon-period**: 11:30 daily (afternoon scaling)

### IAM Role
- **eks-scaling-lambda-role**: Minimal required permissions
- **Policies**: EKS, DynamoDB, CloudWatch access

## 🔧 Customization Points

### Schedule Modification
```python
# In DynamoDB eks-scaling-config table
{
  "schedules": {
    "sleep_time": {"start_hour": 1, "end_hour": 6},
    "peak_time": {"weekday": 1, "big_nodes": 3}
  }
}
```

### Node Configuration
```python
# Nodegroup limits and instance types
{
  "nodegroup_limits": {
    "small_nodegroup": {"min_size": 0, "max_size": 1},
    "big_nodegroup": {"min_size": 0, "max_size": 5}
  }
}
```

### Timezone Adjustment
```python
# In lambda_function.py
def get_local_time():
    utc_now = datetime.now(timezone.utc)
    local_timezone = timezone(timedelta(hours=-3))  # Adjust offset
    return utc_now.astimezone(local_timezone)
```

## 📈 Scalability Considerations

### Multi-Cluster Support
- Extend configuration schema for multiple clusters
- Add cluster selection logic in Lambda function
- Implement cluster-specific IAM permissions

### Multi-Region Deployment
- Deploy Lambda functions in each region
- Replicate DynamoDB configuration across regions
- Adjust EventBridge rules for local timezones

### Advanced Scheduling
- Add holiday calendar integration
- Implement weather-based scaling
- Support for multiple peak periods per day

## 🔐 Security Best Practices

### Code Security
- No hardcoded credentials or sensitive data
- Input validation and sanitization
- Secure error handling (no sensitive data in logs)

### AWS Security
- Least-privilege IAM policies
- Resource-specific ARN targeting
- VPC endpoints for private communication (optional)

### Operational Security
- Configuration change auditing
- Access logging and monitoring
- Regular security reviews and updates

---

**Architecture**: Serverless, event-driven, configuration-managed
**Deployment**: Infrastructure as Code (boto3)
**Monitoring**: CloudWatch + DynamoDB audit trail
**Maintenance**: Zero-downtime configuration updates
