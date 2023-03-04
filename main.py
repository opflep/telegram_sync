import os
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync
from telethon import functions, types

load_dotenv()
# replace the values with your own API ID, API HASH and phone number
api_id = os.getenv("APP_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")

with TelegramClient('session_name', api_id, api_hash) as client:
    client.start()

    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Enter the code: '))

    # get all the unread messages in the user's dialog list
    x = [[d.unread_count, d.title] for d in client.get_dialogs() if not getattr(
        d.entity, 'is_private', False) and d.unread_count != 0]


    dialogs, entities = client.get_dialogs(limit=None, dialogs=None)

    # iterate over the dialogs and get the unread messages in each dialog
    for dialog, entity in zip(dialogs, entities):
        if dialog.unread_count > 0:
            messages = client.get_messages(entity, limit=dialog.unread_count)
            for message in messages:
                print(f'{message.sender.first_name} {message.sender.last_name}: {message.message}')
