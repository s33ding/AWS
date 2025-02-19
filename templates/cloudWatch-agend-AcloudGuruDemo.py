1. Bootstrap script: 
#!/bin/bash	
dnf update -y	

2. Log in to the instance and install rsyslog, which will generate a readable text file of the operating system messages in /var/log/messages. 

sudo su  
dnf install rsyslog
systemctl start rsyslog
systemctl enable rsyslog

3. Install the CW Agent: 
dnf install amazon-cloudwatch-agent -y

4. Configure the CW agent: 
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

****Say no to monitoring CollectD****
Monitor /var/log/messages

5. View the CloudWatch agent config file:
cd /opt/aws/amazon-cloudwatch-agent/bin
cat config.json

6. Start the CloudWatch Agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json

7. Generate some activity on our system by installing stress:
dnf install stress -y
stress --cpu 1

### ref: https://github.com/ACloudGuru-Resources/course-aws-certified-developer-associate/blob/main/CloudWatch_Demo/AL2023_Commands.txt
