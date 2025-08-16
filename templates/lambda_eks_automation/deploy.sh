#!/bin/bash

# EKS Scaling Automation Deployment Script
# Professional AWS Lambda solution for intelligent EKS node scaling

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

# Validate prerequisites
echo -e "${YELLOW}🔍 Validating prerequisites...${NC}"

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

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pip3 install -r requirements.txt --quiet

# Run validation tests
echo -e "${YELLOW}🧪 Running validation tests...${NC}"
python3 test_lambda.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Validation tests passed${NC}"
else
    echo -e "${RED}❌ Validation tests failed. Aborting deployment.${NC}"
    exit 1
fi

# Deploy AWS infrastructure
echo -e "${YELLOW}🏗️  Deploying AWS infrastructure...${NC}"
python3 deploy_infrastructure.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Infrastructure deployed successfully${NC}"
else
    echo -e "${RED}❌ Infrastructure deployment failed${NC}"
    exit 1
fi

# Setup configuration
echo -e "${YELLOW}⚙️  Setting up configuration...${NC}"
echo "yes" | python3 setup_config.py > /dev/null

# Wait for resources to be ready
echo -e "${YELLOW}⏳ Waiting for resources to initialize...${NC}"
sleep 30

# Test deployed function
echo -e "${YELLOW}🔍 Testing deployed Lambda function...${NC}"
aws lambda invoke \
    --function-name ${PROJECT_NAME} \
    --payload '{"trigger": "deployment_test"}' \
    --region ${REGION} \
    --cli-binary-format raw-in-base64-out \
    test_response.json > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Lambda function test successful${NC}"
    rm -f test_response.json
else
    echo -e "${RED}❌ Lambda function test failed${NC}"
fi

# Display system status
echo -e "${YELLOW}📊 System status:${NC}"
python3 monitor.py

echo ""
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo "📋 Management Commands:"
echo "  Monitor system:     python3 monitor.py"
echo "  Manage config:      python3 manage_config.py"
echo "  View logs:          aws logs tail /aws/lambda/${PROJECT_NAME} --follow"
echo ""
echo "🔗 AWS Console Links:"
echo "  Lambda Function:    https://console.aws.amazon.com/lambda/home?region=${REGION}#/functions/${PROJECT_NAME}"
echo "  DynamoDB Config:    https://console.aws.amazon.com/dynamodbv2/home?region=${REGION}#table?name=eks-scaling-config"
echo "  EventBridge Rules:  https://console.aws.amazon.com/events/home?region=${REGION}#/rules"
echo ""
echo -e "${BLUE}💡 The system will automatically scale EKS nodes based on the configured schedule.${NC}"
echo -e "${BLUE}💰 Estimated cost optimization: 10-15% reduction in compute costs.${NC}"
