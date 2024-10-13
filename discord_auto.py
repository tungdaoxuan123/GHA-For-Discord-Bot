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

def fetch_last_message():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        messages = response.json()
        data = messages[0] if messages else {}
        if data:
            description = data['embeds'][0]['description']
            match = re.search(r'\*\*(\d+)\*\*', description)

            if match:
                kakera = match.group(1)
                return kakera
            else:
                print("No number found.")
                return 0
    
                

def send_text(text):
    payload = {
        "content": text
    }
    response = requests.post(url, json=payload, headers=headers)

send_text("tungdao GHA: start roll")
send_text("$w")
kakera = fetch_last_message()
send_text(f"Kakera is : {kakera}")
