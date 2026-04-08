# AWS Q CLI Cheat Sheet

## Installation & Setup

```bash
# Install AWS CLI v2 (required for Q)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
```

## Basic Q Commands

### Chat with Q
```bash
# Start interactive chat
aws q chat

# Ask a single question
aws q chat --message "How do I create an S3 bucket?"

# Chat with specific context
aws q chat --message "Optimize this Lambda function" --context-file lambda.py
```

### Code Analysis
```bash
# Analyze current directory
aws q analyze

# Analyze specific file
aws q analyze --file app.py

# Analyze with custom prompt
aws q analyze --file app.py --prompt "Find security issues"
```

### Code Generation
```bash
# Generate code from description
aws q generate --prompt "Create a Python function to upload files to S3"

# Generate with specific language
aws q generate --prompt "REST API endpoint" --language python

# Generate infrastructure code
aws q generate --prompt "CloudFormation template for VPC" --type infrastructure
```

## Advanced Features

### Context Management
```bash
# Add file context
aws q chat --context-file config.yaml --message "Review this configuration"

# Add multiple files
aws q chat --context-file "*.py" --message "Review Python code"

# Include directory context
aws q chat --context-dir ./src --message "Analyze project structure"
```

### Code Review
```bash
# Review changes
aws q review

# Review specific commit
aws q review --commit abc123

# Review with focus
aws q review --focus security
```

### Explain Code
```bash
# Explain current file
aws q explain

# Explain specific function
aws q explain --function main --file app.py

# Explain with context
aws q explain --line-range 10-20 --file script.py
```

## Output Options

```bash
# JSON output
aws q chat --message "List EC2 instances" --output json

# Save to file
aws q generate --prompt "Docker setup" --output-file Dockerfile

# Verbose mode
aws q analyze --verbose
```

## Configuration

```bash
# Set default model
aws q configure set model claude-3

# Set output format
aws q configure set output-format markdown

# View current config
aws q configure list
```

## Common Use Cases

### AWS Resource Help
```bash
aws q chat --message "How to set up Auto Scaling?"
aws q chat --message "Best practices for RDS security"
aws q chat --message "Cost optimization for EC2"
```

### Debugging
```bash
aws q chat --context-file error.log --message "Help debug this error"
aws q analyze --file broken-script.py --focus bugs
```

### Documentation
```bash
aws q generate --prompt "API documentation for this function" --context-file api.py
aws q explain --file complex-algorithm.py --output-file README.md
```

## Tips & Shortcuts

- Use `--help` with any command for detailed options
- Press `Ctrl+C` to exit interactive chat
- Use `--dry-run` to preview actions without executing
- Combine `--context-file` with wildcards for multiple files
- Use `--format` to specify output format (markdown, json, text)

## Environment Variables

```bash
export AWS_Q_MODEL="claude-3-sonnet"
export AWS_Q_OUTPUT_FORMAT="markdown"
export AWS_Q_CONTEXT_LIMIT="10000"
```