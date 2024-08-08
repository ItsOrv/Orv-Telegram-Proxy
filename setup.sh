#!/bin/bash

# welcome message
echo "Welcome to Orv Telegram Proxy Scraper setup script!"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit
fi

# Create a virtual environment (optional but recommended)
if ! [ -d "venv" ]; then
    echo "Creating a virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Prompt the user for necessary API credentials
echo "Please provide the following information to configure your environment."

read -p "API ID: " API_ID
read -p "API Hash: " API_HASH
read -p "Bot Token: " BOT_TOKEN
read -p "Session Name (default: 'session_name'): " SESSION_NAME

# Default value for SESSION_NAME if not provided
if [ -z "$SESSION_NAME" ]; then
    SESSION_NAME="session_name"
fi

# Create the .env file
echo "Creating the .env file..."
cat > .env <<EOL
API_ID=$API_ID
API_HASH=$API_HASH
BOT_TOKEN=$BOT_TOKEN
SESSION_NAME=$SESSION_NAME
EOL

echo ".env file created successfully!"

# Finish setup
echo "Setup is complete. You can now run your bot using:"
echo "source venv/bin/activate"
echo "python src/bot.py"

# Deactivate virtual environment
deactivate
