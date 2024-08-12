import json
from config import db_path

def save_data(data):
    with open(db_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_data():
    with open(db_path, 'r') as file:
        return json.load(file)

async def refresh_groups(client):
    dialogs = await client.get_dialogs()
    data = load_data()
    all_channel_ids = set(dialog.id for dialog in dialogs if dialog.is_channel)
    existing_channels = set(data['target_channels'])
    
    new_channels = all_channel_ids - existing_channels
    data['target_channels'].extend(new_channels)

    save_data(data)
