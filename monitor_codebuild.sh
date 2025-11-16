#!/bin/bash

# Data IESB CodeBuild Monitoring Dashboard
# Usage: ./monitor_codebuild.sh [project_name]

PROJECT_NAME=${1:-""}
REFRESH_INTERVAL=30

clear
echo "🚀 DATA IESB - CODEBUILD MONITORING DASHBOARD"
echo "=============================================="
echo "Refresh Interval: ${REFRESH_INTERVAL}s | Press Ctrl+C to exit"
echo ""

while true; do
    echo "📊 CURRENT STATUS - $(date)"
    echo "----------------------------------------"
    
    # Get recent builds
    if [ -n "$PROJECT_NAME" ]; then
        echo "🔍 Monitoring Project: $PROJECT_NAME"
        python3 /home/roberto/Github/aws/codebuild-get_status.py 3 $PROJECT_NAME
    else
        echo "🔍 Monitoring All Projects (Latest 5 builds)"
        python3 /home/roberto/Github/aws/codebuild-get_status.py 5
    fi
    
    echo ""
    echo "🔄 Next refresh in ${REFRESH_INTERVAL}s..."
    echo "=========================================="
    
    sleep $REFRESH_INTERVAL
    clear
done
