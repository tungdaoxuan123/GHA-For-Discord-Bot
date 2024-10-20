import os
import json
import re
import requests
import time

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

            kakera = int(match.group(1)) if match else "No number found."
            emoji = None
            if 'components' in data:
                for component in data['components']:
                    for subcomponent in component['components']:
                        if 'emoji' in subcomponent and subcomponent['emoji']:
                            emoji = subcomponent['emoji']['name']
                            break
            return kakera, emoji, data['id'], data['components']  # Return message ID and components
        else:
            print("No messages found.")
            return 0, None, None, None  # Return 0 and None if no data
    else:
        print(f"Failed to fetch messages. Status code: {response.status_code}, Response: {response.text}")
        return 0, None, None, None  # Return 0 and None on failure

def interact_with_message(channel_id, message_id, custom_id, user_token):
    url = f'https://discord.com/api/v9/interactions'
    headers = {
        'Authorization': user_token,
        'Content-Type': 'application/json'
    }
    payload = {
        "type": 2,  # Type for button interaction
        "guild_id": "YOUR_GUILD_ID",  # Optional: ID of the guild
        "channel_id": channel_id,  # The channel ID
        "message_id": message_id,  # The message ID containing the button
        "data": {
            "component_type": 2,  # Type of component (button)
            "custom_id": custom_id  # Custom ID of the button
        }
    }

    response = requests.post(url, json=payload, headers=headers)  # Send POST request to interact
    if response.status_code == 204:
        print(f"Successfully interacted with message {message_id}.")
    else:
        print(f"Failed to interact. Status code: {response.status_code}, Response: {response.text}")

def send_text(text):
    payload = {
        "content": text
    }
    response = requests.post(url, json=payload, headers=headers)

def start_roll():
    send_text("tungdao GHA: start roll")
    max_kakera = 0
    target_position = -1
    target_message_id = None
    target_custom_id = None  # Store the custom ID of the button

    try:
        for i in range(8):
            send_text("$w")
            time.sleep(3)
            kakera, emoji, message_id, components = fetch_last_message(url, headers)

            if isinstance(kakera, int):
                send_text(f"Kakera is: {kakera}")
                send_text(f"Emoji is: {emoji}")

                if kakera > max_kakera:
                    target_position = i
                    max_kakera = kakera
                    target_message_id = message_id  # Store the message ID of the highest kakera

                    # Extract custom_id from components
                    if components:
                        for component in components:
                            for subcomponent in component['components']:
                                if 'custom_id' in subcomponent:
                                    target_custom_id = subcomponent['custom_id']  # Get the custom ID of the button
                                    break
            else:
                send_text("Invalid kakera value. Stopping roll.")
                break
    except Exception as e:
        send_text(f"An error occurred: {e}")
    finally:
        send_text("tungdao GHA: stop roll")

        # Interact with the message with the highest kakera
        if target_message_id and target_custom_id:
            interact_with_message(channel_id, target_message_id, target_custom_id, user_token)

start_roll()
