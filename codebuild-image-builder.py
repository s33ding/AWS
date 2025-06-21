#!/bin/bash

# === CONFIGURATION ===
ACCOUNT_ID="248189947068"
REGION="us-east-1"
REPO_NAME="codebuild-tools"
IMAGE_TAG="latest"
ECR_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME"

# === AUTHENTICATE WITH ECR ===
echo "Authenticating with ECR in region $REGION..."
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

# === CREATE REPO IF NOT EXISTS ===
echo "Ensuring ECR repository exists..."
aws ecr describe-repositories --repository-names "$REPO_NAME" --region "$REGION" >/dev/null 2>&1 || \
aws ecr create-repository --repository-name "$REPO_NAME" --region "$REGION"

# === BUILD DOCKER IMAGE ===
echo "Building Docker image with kubectl and awscli..."
cat <<'EOF' > Dockerfile
FROM amazonlinux:2023

# Install base tools
RUN yum -y update && \
    yum install -y unzip curl tar gzip python3 pip shadow-utils --allowerasing && \
    pip3 install --upgrade awscli

# Install Docker CLI & Daemon
RUN yum install -y docker

RUN curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && mv kubectl /usr/local/bin/

CMD ["bash"]
EOF


docker build -t "$REPO_NAME:$IMAGE_TAG" .

# === TAG AND PUSH TO ECR ===
echo "Tagging and pushing image to ECR..."
docker tag "$REPO_NAME:$IMAGE_TAG" "$ECR_URI:$IMAGE_TAG"
docker push "$ECR_URI:$IMAGE_TAG"

# === CLEANUP ===
rm -f Dockerfile

echo "✅ Image pushed: $ECR_URI:$IMAGE_TAG"


