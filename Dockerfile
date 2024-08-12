# Use a specific version of the Python slim image for better reliability
FROM python:3.10.0-slim-buster

# Set the working directory in the Docker container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python packages from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's source code into the container
COPY . .

# Command to run the application
CMD ["python", "src/bot.py"]
