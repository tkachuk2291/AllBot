import asyncio
import logging
import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

from logsetup import set_context, setup_logging

load_dotenv()
setup_logging("all-bot")
log = logging.getLogger("all-bot")

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session_name = os.getenv("SESSION_NAME", "my_session")
os.makedirs(os.path.dirname(session_name) or ".", exist_ok=True)

client = TelegramClient(session_name, api_id, api_hash, connection_retries=-1, retry_delay=10)


@client.on(events.NewMessage(pattern=r"^\.all$", outgoing=True))
async def tag_all(event):
    set_context(chat_id=event.chat_id)
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
    log.info("Tagged %d members", len(mentions), extra={"members": len(mentions)})


client.start()
log.info("Bot started, waiting for .all")
client.run_until_disconnected()
