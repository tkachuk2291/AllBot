import asyncio
import getpass
import os

import qrcode
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import PasswordHashInvalidError, SessionPasswordNeededError

load_dotenv()

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session_name = os.getenv("SESSION_NAME", "my_session")
os.makedirs(os.path.dirname(session_name) or ".", exist_ok=True)


def show_qr(url):
    print("\033[2J\033[H", end="")
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.print_ascii(invert=True)
    print("Telegram на телефоне → Настройки → Устройства → Подключить устройство")
    print("QR обновляется каждые 30 секунд")


async def enter_password(client):
    while True:
        try:
            await client.sign_in(password=getpass.getpass("Пароль 2FA (облачный пароль Telegram): "))
            return
        except PasswordHashInvalidError:
            print("Неверный пароль, попробуй ещё раз.")


async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()

    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"Уже авторизован как {me.first_name} (@{me.username})")
        await client.disconnect()
        return

    try:
        qr_login = await client.qr_login()
        while True:
            show_qr(qr_login.url)
            try:
                await qr_login.wait(timeout=30)
                break
            except asyncio.TimeoutError:
                await qr_login.recreate()
    except SessionPasswordNeededError:
        await enter_password(client)

    me = await client.get_me()
    print(f"Готово! Вошёл как {me.first_name} (@{me.username}). Теперь запускай main.py")
    await client.disconnect()


asyncio.run(main())
