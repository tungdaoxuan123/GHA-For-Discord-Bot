import os
import json
import re
import requests

user_token = os.environ["DISCORD_USER_TOKEN"]
channel_id = os.environ["CHANNEL_ID"]

url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

# Set up the request headers
headers = {
    "Authorization": user_token,
    "Content-Type": "application/json"  # Set content type to JSON
}

def fetch_last_message(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        messages = response.json()
        data = messages[0] if messages else {}
        if data:
            description = data['embeds'][0]['description']
            match = re.search(r'\*\*(\d+)\*\*', description)

            kakera = match.group(1) if match else "No number found."
            emoji = None
            if 'components' in data:
                for component in data['components']:
                    for subcomponent in component['components']:
                        if 'emoji' in subcomponent and subcomponent['emoji']:
                            emoji = subcomponent['emoji']['name']
                            break
            return kakera, emoji
        else:
            print("No messages found.")
            return 0, None  # Return 0 and None if no data
    else:
        print(f"Failed to fetch messages. Status code: {response.status_code}, Response: {response.text}")
        return 0, None  # Return 0 and None on failure


def react_to_message(channel_id, message_id, emoji_id, user_token):
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji_id}/@me'
    headers = {
        'Authorization': user_token,
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers)  # Use PUT to add a reaction
              

def send_text(text):
    payload = {
        "content": text
    }
    response = requests.post(url, json=payload, headers=headers)

def start_roll():
    send_text("tungdao GHA: start roll")
    max_kakera = 0
    target_position = 0
    for i in range(0, 8):
        send_text("$w")
        kakera, emoji = fetch_last_message()
        send_text(f"Kakera is : {kakera}")
        send_text(f"emoji is : {emoji}")
        if kakera > max_kakera:
            target_position = i
            max_kakera = kakera
    send_text("tungdao GHA: stop roll")