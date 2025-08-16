#!/bin/bash

# EKS Scaling Automation Deployment Script
# Author: Roberto
# Description: Deploy complete EKS scaling automation infrastructure

set -e  # Exit on any error

echo "🚀 EKS Scaling Automation Deployment"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REGION="sa-east-1"
PROJECT_NAME="eks-scaling-automation"

echo -e "${BLUE}Region: ${REGION}${NC}"
echo -e "${BLUE}Project: ${PROJECT_NAME}${NC}"
echo ""

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install AWS CLI first.${NC}"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials not configured. Please run 'aws configure' first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ AWS CLI configured${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3 first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 available${NC}"

# Install Python dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
pip3 install -r requirements.txt --quiet

# Run tests first
echo -e "${YELLOW}🧪 Running tests...${NC}"
python3 test_lambda.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Tests passed${NC}"
else
    echo -e "${RED}❌ Tests failed. Aborting deployment.${NC}"
    exit 1
fi

# Deploy infrastructure
echo -e "${YELLOW}🏗️  Deploying infrastructure...${NC}"
python3 deploy_infrastructure.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Infrastructure deployed successfully${NC}"
else
    echo -e "${RED}❌ Infrastructure deployment failed${NC}"
    exit 1
fi

# Wait for resources to be ready
echo -e "${YELLOW}⏳ Waiting for resources to be ready...${NC}"
sleep 30

# Test the deployed Lambda function
echo -e "${YELLOW}🔍 Testing deployed Lambda function...${NC}"
aws lambda invoke \
    --function-name ${PROJECT_NAME} \
    --payload '{"trigger": "deployment_test"}' \
    --region ${REGION} \
    --cli-binary-format raw-in-base64-out \
    test_response.json

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Lambda function test successful${NC}"
    echo "Response:"
    cat test_response.json | python3 -m json.tool
    rm test_response.json
else
    echo -e "${RED}❌ Lambda function test failed${NC}"
fi

# Run monitoring to show current status
echo -e "${YELLOW}📊 Current system status:${NC}"
python3 monitor.py

echo ""
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo "📋 Next steps:"
echo "1. Monitor the system: python3 monitor.py"
echo "2. Check CloudWatch logs: https://console.aws.amazon.com/cloudwatch/home?region=${REGION}#logsV2:log-groups/log-group/\$252Faws\$252Flambda\$252F${PROJECT_NAME}"
echo "3. View DynamoDB table: https://console.aws.amazon.com/dynamodbv2/home?region=${REGION}#table?name=eks-scaling-logs"
echo "4. Check Lambda function: https://console.aws.amazon.com/lambda/home?region=${REGION}#/functions/${PROJECT_NAME}"
echo ""
echo -e "${BLUE}💡 The system will automatically scale your EKS nodes based on the São Paulo timezone schedule.${NC}"
echo -e "${BLUE}💰 Estimated monthly savings: ~$68.64 (13.9%)${NC}"
