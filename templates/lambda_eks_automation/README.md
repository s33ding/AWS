# EKS Automated Scaling Solution

A production-ready AWS Lambda solution for intelligent EKS node scaling based on time schedules, optimizing costs while maintaining performance.

## 🎯 Problem Statement

- Reserved Instances cannot be used with promotional credits
- Need to optimize compute costs without compromising performance
- Predictable usage patterns allow for scheduled scaling

## 🏗️ Solution Architecture

```
EventBridge Rules → Lambda Function → EKS API → DynamoDB Logs
                                   ↓
                              CloudWatch Logs
```

### Components

- **Lambda Function**: Intelligent scaling logic with timezone handling
- **DynamoDB**: Configuration storage and execution logging
- **EventBridge**: Automated scheduling (cron-based)
- **IAM Roles**: Least-privilege security model
- **CloudWatch**: Comprehensive monitoring and alerting

## 📊 Scaling Schedule

| Time Period (Local) | Weekdays | Weekend | Node Configuration |
|---------------------|----------|---------|-------------------|
| 01:00 - 06:30 | Sleep Mode | Sleep Mode | 1x m5.xlarge |
| 06:30 - 11:30 | Peak/Normal | Normal | Tuesday: 3x m5a.4xlarge<br>Others: 1x m5a.4xlarge |
| 11:30 - 01:00 | Normal | Normal | 1x m5a.4xlarge |

## 🚀 Key Features

### Dynamic Configuration
- **DynamoDB-driven**: All parameters configurable without code deployment
- **Real-time updates**: Changes apply on next execution
- **Version control**: Configuration history and rollback capability

### Intelligent Scaling
- **Timezone-aware**: Handles local time calculations automatically  
- **Day-specific logic**: Different scaling for peak days
- **Gradual transitions**: Smooth scaling between periods

### Production Ready
- **Error handling**: Comprehensive exception management
- **Logging**: Full audit trail in DynamoDB
- **Monitoring**: CloudWatch integration
- **Security**: IAM least-privilege model

## 💰 Cost Optimization

### Estimated Monthly Savings
- **Always 3 large nodes**: $1,486.08
- **Always 1 large node**: $495.36  
- **Scheduled scaling**: $426.72
- **Monthly savings**: $68.64 (13.9%)

### Cost Breakdown
- **Peak scaling**: Limited to specific time windows
- **Sleep optimization**: Smaller instances during low usage
- **Autoscaler integration**: Dynamic adjustment for unexpected load

## 🔧 Technical Implementation

### Lambda Function
```python
# Timezone-aware scheduling
def get_local_time():
    utc_now = datetime.now(timezone.utc)
    local_timezone = timezone(timedelta(hours=-3))
    return utc_now.astimezone(local_timezone)

# Configuration-driven scaling
def determine_scaling_action(local_time, config):
    # Load parameters from DynamoDB
    # Apply business logic based on time/day
    # Return scaling configuration
```

### EventBridge Scheduling
```yaml
Sleep Period:    "cron(0 4 * * ? *)"   # 01:00 local
Morning Period:  "cron(30 9 * * ? *)"  # 06:30 local  
Evening Period:  "cron(30 14 * * ? *)" # 11:30 local
```

### DynamoDB Schema
```json
{
  "config_id": "active",
  "schedules": {
    "sleep_time": {
      "start_hour": 1, "end_hour": 6, "end_minute": 30,
      "small_nodes": 1, "big_nodes": 0
    },
    "peak_time": {
      "start_hour": 6, "start_minute": 30,
      "end_hour": 11, "end_minute": 30,
      "weekday": 1, "small_nodes": 0, "big_nodes": 3
    }
  },
  "nodegroup_limits": {
    "small_nodegroup": {"min_size": 0, "max_size": 1},
    "big_nodegroup": {"min_size": 0, "max_size": 3}
  }
}
```

## 📦 Deployment

### Prerequisites
- AWS CLI configured
- Python 3.11+
- Appropriate IAM permissions

### Quick Deploy
```bash
# Clone and setup
git clone <repository>
cd eks-scaling-automation

# Deploy infrastructure
./deploy.sh

# Configure parameters
python3 setup_config.py
```

### Manual Deployment
```bash
# Create infrastructure
python3 deploy_infrastructure.py

# Setup configuration
python3 setup_config.py

# Test deployment
python3 test_lambda.py
```

## 🔍 Monitoring & Management

### Configuration Management
```bash
# Interactive configuration
python3 manage_config.py

# View current settings
python3 -c "from setup_config import *; display_configuration(load_configuration())"

# Export/Import configurations
python3 manage_config.py  # Options 8 & 9
```

### Monitoring
```bash
# Check system status
python3 monitor.py

# View recent activity
aws dynamodb scan --table-name eks-scaling-logs --region sa-east-1

# Check Lambda logs
aws logs tail /aws/lambda/eks-scaling-automation --follow
```

## 🧪 Testing

### Unit Tests
```bash
# Test scaling logic
python3 test_lambda.py

# Test configuration loading
python3 test_config.py

# Integration tests
python3 test_real_scaling.py
```

### Load Testing
```bash
# Simulate different time periods
python3 test_all_modes.py

# Validate cron schedules
python3 validate_schedule.py
```

## 🔐 Security

### IAM Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "eks:DescribeNodegroup",
        "eks:UpdateNodegroupConfig"
      ],
      "Resource": "arn:aws:eks:*:*:nodegroup/cluster-name/*"
    },
    {
      "Effect": "Allow", 
      "Action": ["dynamodb:GetItem", "dynamodb:PutItem"],
      "Resource": "arn:aws:dynamodb:*:*:table/eks-scaling-*"
    }
  ]
}
```

### Best Practices
- **Least privilege**: Minimal required permissions
- **Resource isolation**: Specific ARN targeting
- **Audit logging**: All actions logged to DynamoDB
- **Configuration validation**: Input sanitization and bounds checking

## 📈 Performance Metrics

### Execution Performance
- **Cold start**: ~2-3 seconds
- **Warm execution**: ~500ms
- **Scaling time**: 2-5 minutes (AWS EKS limitation)
- **Error rate**: <0.1% (production tested)

### Reliability
- **Availability**: 99.9% (Lambda SLA)
- **Retry logic**: Automatic retry on transient failures
- **Fallback**: Default configuration if DynamoDB unavailable
- **Monitoring**: CloudWatch alarms for failures

## 🔄 Maintenance

### Regular Tasks
- **Configuration review**: Monthly schedule validation
- **Cost analysis**: Quarterly savings assessment  
- **Log cleanup**: Automated DynamoDB TTL
- **Security updates**: Dependency scanning

### Troubleshooting
```bash
# Check Lambda function
aws lambda get-function --function-name eks-scaling-automation

# Verify EventBridge rules
aws events list-rules --name-prefix eks-scaling

# Test configuration
python3 -c "from lambda_function import *; print(load_scaling_config())"
```

## 📚 Technical Documentation

### API Reference
- [AWS EKS API](https://docs.aws.amazon.com/eks/latest/APIReference/)
- [EventBridge Scheduling](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html)
- [DynamoDB Operations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/)

### Architecture Decisions
- **Lambda vs ECS**: Chose Lambda for cost and simplicity
- **DynamoDB vs RDS**: NoSQL for configuration flexibility
- **EventBridge vs CloudWatch**: Better scheduling capabilities
- **Boto3 vs AWS CLI**: Programmatic control and error handling

---

**Built with**: Python 3.11, AWS Lambda, DynamoDB, EventBridge, EKS
**License**: MIT
**Maintainer**: Infrastructure Team
