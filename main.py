import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session_name = os.getenv("SESSION_NAME", "my_session")
os.makedirs(os.path.dirname(session_name) or ".", exist_ok=True)

client = TelegramClient(session_name, api_id, api_hash)


@client.on(events.NewMessage(pattern=r"^\.all$", outgoing=True))
async def tag_all(event):
    await event.delete()
    mentions = []
    async for user in client.iter_participants(event.chat_id):
        if user.bot or user.deleted or user.is_self:
            continue
        name = user.first_name or "user"
        mentions.append(f'<a href="tg://user?id={user.id}">{name}</a>')

    for i in range(0, len(mentions), 5):
        await client.send_message(event.chat_id, " ".join(mentions[i:i+5]), parse_mode="html")
        await asyncio.sleep(1)


client.start()
print("Бот запущен. Напиши .all в любом чате.")
client.run_until_disconnected()
