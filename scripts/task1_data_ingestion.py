import asyncio
import os
import re
import pandas as pd
from telethon import TelegramClient, events
from telethon.errors import PeerFloodError, FloodWaitError

# --- Configuration ---
API_ID = 26959383  # Replace with your API ID
API_HASH = "466a3971dfb79c38346f5cacd64b88e3"  # Replace with your API Hash
SESSION_NAME = "scraper_session"

MAX_MESSAGES_PER_CHANNEL = 1000

# Initialize Telethon client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# --- Functions ---

def preprocess_amharic_text(text):
    # Keep only Amharic Unicode characters and spaces
    text = re.sub(r'[^\u1200-\u137F\s]', '', text)
    return text.strip()

async def fetch_telegram_messages(channel):
    print(f"📥 Fetching up to {MAX_MESSAGES_PER_CHANNEL} messages from @{channel}")
    messages = []
    try:
        async for message in client.iter_messages(channel, limit=MAX_MESSAGES_PER_CHANNEL):
            if message.text:
                cleaned_text = preprocess_amharic_text(message.text)
                if cleaned_text:
                    messages.append({"channel": channel, "text": cleaned_text})
    except FloodWaitError as e:
        print(f"⚠️ Flood wait error. Need to wait {e.seconds} seconds before trying again.")
    except Exception as e:
        print(f"❌ Error fetching from @{channel}: {str(e)}")
    return messages

async def main():
    channels = [
        "shageronlinestore",
        "ethiopian_market_1",
        "ZemenExpress",
        "nevacomputer",
        "meneshayeofficial",
        "ethio_brand_collection",
        "Leyueqa",
        "sinayelj",
        "Shewabrand",
        "helloomarketethiopia",
        "modernshoppingcenter",
        "qnashcom",
        "Fashiontera",
        "kuruwear",
        "gebeyaadama",
        "MerttEka",
        "forfreemarket",
        "classybrands",
        "marakibrand",
        "aradabrand2",
        "marakisat2",
        "belaclassic",
        "AwasMart"
    ]

    all_messages = []

    print("🔌 Connecting to Telegram...")
    await client.start()
    print("✅ Connected successfully.")

    tasks = [fetch_telegram_messages(channel) for channel in channels]
    results = await asyncio.gather(*tasks)

    for result in results:
        all_messages.extend(result)

    # Save to CSV
    output_dir = "../data/processed"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "cleaned_data.csv")

    df = pd.DataFrame(all_messages)
    df.to_csv(output_file, index=False)

    print(f"📦 Data saved to: {os.path.abspath(output_file)}")
    print(f"📊 Total messages scraped: {len(all_messages)}")

if __name__ == "__main__":
    asyncio.run(main())