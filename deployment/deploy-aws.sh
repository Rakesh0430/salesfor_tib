#!/bin/bash

# Exit on any error
set -e

echo "Starting AWS deployment for MSdynamics..."

# Create key pair
aws ec2 create-key-pair \
    --key-name msdynamics-key \
    --query 'KeyMaterial' \
    --output text > msdynamics-key.pem

chmod 400 msdynamics-key.pem

echo "Created key pair: msdynamics-key"

# Create security group
aws ec2 create-security-group \
    --group-name msdynamics-sg \
    --description "Security group for MSdynamics Salesforce Service"

SG_ID=$(aws ec2 describe-security-groups \
    --group-names msdynamics-sg \
    --query 'SecurityGroups[0].GroupId' \
    --output text)

echo "Created security group: $SG_ID"

# Configure security group rules
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0

echo "Configured security group rules"

# Launch EC2 instance
echo "Launching EC2 instance..."

INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0c7217cdde317cfec \
    --count 1 \
    --instance-type t2.micro \
    --key-name msdynamics-key \
    --security-group-ids $SG_ID \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=msdynamics-service}]' \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "Waiting for instance to be running..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "EC2 instance is ready!"
echo "Instance ID: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"

echo "Next steps:"
echo "1. Create project directory on EC2:"
echo "   ssh -i msdynamics-key.pem ec2-user@$PUBLIC_IP 'mkdir -p ~/msdynamics/src/logs'"

echo "2. Copy project files:"
echo "   scp -i msdynamics-key.pem -r src config requirements.txt ec2-user@$PUBLIC_IP:~/msdynamics/"
echo "   scp -i msdynamics-key.pem deployment/setup-ec2.sh ec2-user@$PUBLIC_IP:~/msdynamics/"
echo "   scp -i msdynamics-key.pem .env ec2-user@$PUBLIC_IP:~/msdynamics/"

echo "3. SSH to instance:"
echo "   ssh -i msdynamics-key.pem ec2-user@$PUBLIC_IP"

echo "4. Run setup script:"
echo "   cd ~/msdynamics && chmod +x setup-ec2.sh && ./setup-ec2.sh"