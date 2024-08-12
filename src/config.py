#config.py
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
admin_id = int(os.getenv('ADMIN_ID', '0'))
db_path = os.getenv('DB_PATH', './data/db.json')

