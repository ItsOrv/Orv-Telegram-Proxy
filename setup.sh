#!/bin/bash

# welcome message
echo "Welcome to Orv Telegram Proxy setup script!"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit
fi

# Create a virtual environment
if ! [ -d "venv" ]; then
    echo "Creating a virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Please provide the following information to configure your environment."
read -p "API ID: " API_ID
read -p "API Hash: " API_HASH
read -p "Bot Token: " BOT_TOKEN

cat > .env <<EOL
API_ID=$API_ID
API_HASH=$API_HASH
BOT_TOKEN=$BOT_TOKEN
EOL

echo ".env file created successfully!"
echo "You can now run the bot with: python bot.py"

deactivate
