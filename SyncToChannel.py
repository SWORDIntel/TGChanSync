#!/usr/bin/env python3

# Activate virtual environment
import sys
import site
import os
venv_path = os.path.join(os.getcwd(), 'venv')
site.addsitedir(os.path.join(venv_path, 'lib', f'python{sys.version[:3]}', 'site-packages'))
os.environ['VIRTUAL_ENV'] = venv_path
os.environ['PATH'] = os.path.join(venv_path, 'bin') + os.pathsep + os.environ['PATH']

import asyncio
from telethon import TelegramClient, errors

api_id = 'X'
api_hash = 'X'
source_channel_id = '@X'  # Replace with the correct channel ID or username
destination_channel_id = '@X'  # Replace with the correct channel ID or username
destination_topic_id = X  # Replace with the correct topic ID (top message ID for the topic)

# File to store the ID of the last forwarded message
last_message_file = 'last_message_id.txt'

# Create the client and connect
client = TelegramClient('forwarder', api_id, api_hash)

async def get_last_message_id():
    if os.path.exists(last_message_file):
        with open(last_message_file, 'r') as f:
            return int(f.read().strip())
    return None

async def set_last_message_id(message_id):
    with open(last_message_file, 'w') as f:
        f.write(str(message_id))

async def forward_messages():
    # Connect to the client
    print("Connecting to Telegram...")
    await client.connect()

    if not await client.is_user_authorized():
        print("Client is not authorized. Please log in manually once to store session.")
        return

    # Get the source and destination channels
    try:
        print(f"Retrieving entity for source channel: {source_channel_id}")
        source_channel = await client.get_entity(source_channel_id)
        print(f"Successfully retrieved source channel: {getattr(source_channel, 'title', str(source_channel))}")
    except (ValueError, errors.UsernameNotOccupiedError, errors.ChannelInvalidError) as e:
        print(f"Cannot find any entity corresponding to the source channel: {source_channel_id}. Error: {e}")
        return

    try:
        print(f"Retrieving entity for destination channel: {destination_channel_id}")
        destination_channel = await client.get_entity(destination_channel_id)
        print(f"Successfully retrieved destination channel: {getattr(destination_channel, 'title', str(destination_channel))}")
    except (ValueError, errors.UsernameNotOccupiedError, errors.ChannelInvalidError) as e:
        print(f"Cannot find any entity corresponding to the destination channel: {destination_channel_id}. Error: {e}")
        return

    # Get the ID of the last forwarded message
    last_message_id = await get_last_message_id()
    if last_message_id:
        print(f"Last forwarded message ID: {last_message_id}")
    else:
        print("No previously forwarded messages found.")

    # Get message history from the source channel
    print("Retrieving message history from the source channel...")
    messages = await client.get_messages(source_channel, min_id=last_message_id, limit=300) if last_message_id else await client.get_messages(source_channel, limit=300)
    messages_to_forward = list(reversed(messages))  # Start from the oldest message
    print(f"Retrieved {len(messages_to_forward)} messages to forward.")

    # Forward messages one by one
    for message in messages_to_forward:
        try:
            if message.text or message.media:
                print(f"Forwarding message ID: {message.id}")
                await client.forward_messages(destination_channel, message)
                await set_last_message_id(message.id)
                print(f"Successfully forwarded message ID: {message.id}")
        except Exception as e:
            print(f"Failed to forward message {message.id}: {e}. Error explanation: {str(e).split(':')[0]}")

    print("All messages have been forwarded and are up to date.")

async def scheduled_forward():
    # Run forward_messages immediately
    await forward_messages()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(scheduled_forward())
