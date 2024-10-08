#!/bin/bash

# Exit on any error
set -e

echo "Setting up MSdynamics application..."

# Update system and install dependencies
sudo yum update -y
sudo yum install python3 python3-pip -y

# Create necessary directories
mkdir -p ~/msdynamics/src/logs

# Install Python dependencies
pip3 install -r ~/msdynamics/requirements.txt

# Create systemd service file
sudo tee /etc/systemd/system/msdynamics.service << EOF
[Unit]
Description=MSdynamics Salesforce Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/msdynamics
Environment=PYTHONPATH=/home/ec2-user/msdynamics
ExecStart=/usr/bin/python3 src/main.py
Restart=always
StandardOutput=append:/home/ec2-user/msdynamics/src/logs/app.log
StandardError=append:/home/ec2-user/msdynamics/src/logs/app.log

[Install]
WantedBy=multi-user.target
EOF

# Create empty log file and set permissions
touch ~/msdynamics/src/logs/app.log
chmod 644 ~/msdynamics/src/logs/app.log

# Start and enable the service
sudo systemctl daemon-reload
sudo systemctl start msdynamics
sudo systemctl enable msdynamics

echo "Setup complete!"
echo "To check status: sudo systemctl status msdynamics"
echo "To view logs: tail -f ~/msdynamics/src/logs/app.log"
echo "To view service logs: sudo journalctl -u msdynamics -f"

# Display initial status
echo "Current service status:"
sudo systemctl status msdynamics