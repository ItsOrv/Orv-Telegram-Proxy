# app.py
from flask import Flask, render_template
import json
import threading
import time

app = Flask(__name__)
PROXY_FILE = 'proxies.json'

# Load proxies from the JSON file
def load_proxies():
    try:
        with open(PROXY_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Background task to refresh the proxies every 15 minutes
def refresh_proxies():
    while True:
        proxies = load_proxies()
        # For demonstration purposes, we're simply reloading the file.
        # Replace this with actual code to update the proxies if needed.
        time.sleep(900)  # 15 minutes

@app.route('/')
def index():
    proxies = load_proxies()
    return render_template('index.html', proxies=proxies)

