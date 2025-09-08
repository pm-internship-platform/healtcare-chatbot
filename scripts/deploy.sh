#!/bin/bash

# AI Health Chatbot Deployment Script
# For AWS EC2 deployment

set -e

echo "Starting deployment of AI Health Chatbot..."

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt-get install -y python3-pip python3-venv nginx git

# Install MongoDB
echo "Installing MongoDB..."
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod

# Create application directory
echo "Setting up application directory..."
sudo mkdir -p /opt/ai-health-chatbot
sudo chown -R $USER:$USER /opt/ai-health-chatbot
cd /opt/ai-health-chatbot

# Clone or copy application code
# (Assuming code is already uploaded or cloned)
# git clone <your-repo> .

# Create virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies for frontend
echo "Installing Node.js dependencies..."
cd frontend
npm install
npm run build:css
cd ..

# Set up environment variables
echo "Configuring environment variables..."
cp .env.example .env
# Edit .env with your actual values

# Set up nginx
echo "Configuring nginx..."
sudo cp deployment/nginx.conf /etc/nginx/sites-available/ai-health-chatbot
sudo ln -sf /etc/nginx/sites-available/ai-health-chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up systemd service
echo "Configuring systemd service..."
sudo cp deployment/ai-health-chatbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ai-health-chatbot
sudo systemctl start ai-health-chatbot

# Train Rasa model
echo "Training Rasa model..."
cd rasa
rasa train
cd ..

# Set up firewall
echo "Configuring firewall..."
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
sudo ufw enable

echo "Deployment completed successfully!"
echo "Application should be available at http://your-server-ip"