import os
import requests

user_token = os.environ["DISCORD_USER_TOKEN"]
channel_id = os.environ["CHANNEL_ID"]

url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

# Set up the request headers
headers = {
    "Authorization": user_token,
    "Content-Type": "application/json"  # Set content type to JSON
}

payload = {
    "content": "text form GHA of repo: https://github.com/tungdaoxuan123/GHA_for_discord_bot"
}

response = requests.post(url, json=payload, headers=headers)
