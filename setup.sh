#!/bin/bash

# Welcome message
echo "Welcome to the Telegram Proxy Scraper setup script!"

# Clone the repository
REPO_URL="https://github.com/yourusername/telegram-proxy-scraper.git"
REPO_NAME="telegram-proxy-scraper"

if [ ! -d "$REPO_NAME" ]; then
    echo "Cloning the repository..."
    git clone "$REPO_URL"
fi

# Navigate into the repository
cd "$REPO_NAME" || { echo "Failed to navigate into the repository."; exit 1; }

# Create a .env file for Docker
echo "Creating the .env file..."
cat > .env <<EOL
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
ADMIN_ID=your_admin_id
EOL

# Create directories for data and config
mkdir -p data

# Create a requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "Creating requirements.txt..."
    echo "telethon" > requirements.txt
    echo "requests" >> requirements.txt
fi

# Create a Dockerfile if it doesn't exist
if [ ! -f "Dockerfile" ]; then
    echo "Creating Dockerfile..."
    cat > Dockerfile <<EOL
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/bot.py"]
EOL
fi

# Create a docker-compose.yml if it doesn't exist
if [ ! -f "docker-compose.yml" ]; then
    echo "Creating docker-compose.yml..."
    cat > docker-compose.yml <<EOL
version: '3.8'

services:
  telegram-bot:
    build: .
    environment:
      - API_ID=${API_ID}
      - API_HASH=${API_HASH}
      - BOT_TOKEN=${BOT_TOKEN}
      - ADMIN_ID=${ADMIN_ID}
      - DB_PATH=/app/data/db.json
    volumes:
      - ./data:/app/data
    restart: unless-stopped
EOL
fi

# Build and start Docker containers
echo "Building and starting Docker containers..."
docker-compose up --build -d

# Finish setup
echo "Setup is complete. The Docker container is now running."
