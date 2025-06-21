from telethon import TelegramClient
import asyncio
import json

class TelegramScraper:
    def __init__(self, api_id, api_hash, phone):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.phone = phone

    async def login(self):
        await self.client.start(self.phone)
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            code = input('Enter the code: ')
            await self.client.sign_in(self.phone, code)

    async def fetch_messages_from_channels(self, channels, limit=10000):
        messages = []
        for channel in channels:
            async for message in self.client.iter_messages(channel, limit=limit):
                if message.text:
                    messages.append({
                        'channel': channel,
                        'text': message.text,
                        'date': str(message.date),
                        'views': message.views or 0
                    })
        return messages

    def save_messages_to_file(self, messages, output_path='raw_data.json'):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)