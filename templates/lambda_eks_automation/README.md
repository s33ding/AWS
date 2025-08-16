# EKS Automated Scaling Solution

Production-ready AWS Lambda solution for intelligent EKS node scaling based on time schedules.

## 🎯 Problem & Solution

**Problem**: Optimize EKS compute costs without Reserved Instances while maintaining performance.

**Solution**: Automated time-based scaling with configurable parameters stored in DynamoDB.

## 🏗️ Architecture

```
EventBridge (Cron) → Lambda Function → EKS API
                           ↓
                    DynamoDB Config & Logs
```

## 📊 Scaling Schedule

| Time Period | Configuration |
|-------------|---------------|
| 01:00-06:30 | 1x m5.xlarge (sleep mode) |
| 06:30-11:30 | Tuesday: 3x m5a.4xlarge / Others: 1x m5a.4xlarge |
| 11:30-01:00 | 1x m5a.4xlarge (normal operation) |

**Cost Savings**: ~15% reduction in compute costs

## 🚀 Quick Deploy

```bash
# Deploy everything
./deploy.sh

# Configure parameters
python3 setup_config.py

# Monitor system
python3 monitor.py
```

## 🔧 Key Features

- **Dynamic Configuration**: Change parameters via DynamoDB without code deployment
- **Timezone Aware**: Handles local time calculations automatically
- **Production Ready**: Comprehensive error handling and logging
- **Secure**: IAM least-privilege model

## 📁 Files

- `lambda_function.py` - Main scaling logic
- `deploy_infrastructure.py` - AWS resource creation
- `setup_config.py` - Configuration management
- `test_lambda.py` - Validation tests
- `monitor.py` - System monitoring

## 🔍 Management

**Configuration**: Edit `eks-scaling-config` table in DynamoDB
**Monitoring**: CloudWatch logs + DynamoDB audit trail
**Testing**: `python3 test_lambda.py`

---
**Tech Stack**: Python 3.11, AWS Lambda, DynamoDB, EventBridge, EKS
