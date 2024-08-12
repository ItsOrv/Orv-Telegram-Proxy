#!/bin/bash

echo "Welcome to the Telegram Bot Setup!"

# Variables
REPO_URL="https://github.com/yourusername/telegram-proxy-scraper.git"
REPO_NAME="telegram-proxy-scraper"

# Clone the repository if it doesn't exist
if [ ! -d "$REPO_NAME" ]; then
    echo "Cloning the repository..."
    git clone "$REPO_URL" || { echo "Failed to clone repository."; exit 1; }
fi

# Navigate into the repository directory
cd "$REPO_NAME" || { echo "Failed to navigate into the repository."; exit 1; }

# Create a .env file with necessary environment variables
echo "Setting up environment variables..."
cat > .env <<EOL
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
ADMIN_ID=your_admin_id
EOL

# Create directories for data
echo "Creating data directories..."
mkdir -p data

# Check for a requirements.txt file and create if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "Creating requirements.txt..."
    echo "telethon" > requirements.txt
    echo "requests" >> requirements.txt
fi

# Create Dockerfile and docker-compose.yml if they don't already exist
[ ! -f "Dockerfile" ] && echo "Creating Dockerfile..." && cp /path/to/your/optimized/Dockerfile .
[ ! -f "docker-compose.yml" ] && echo "Creating docker-compose.yml..." && cp /path/to/your/optimized/docker-compose.yml .

# Build and start Docker containers
echo "Building and starting Docker containers..."
docker-compose up --build -d

echo "Setup is complete. The Docker container is now running."
