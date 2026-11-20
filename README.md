# AllBot

Telegram userbot (Telethon, runs as your own account, not a bot token). Send `.all` in any chat and the message is deleted and replaced with mentions of every member, in batches of five.

## How it works

- `main.py` listens for your own outgoing `.all` messages, deletes the command, walks the chat's participants with `iter_participants`, skips bots, deleted accounts and yourself, and posts `tg://user?id=...` mentions five at a time with a one-second pause.
- The Telethon client reconnects forever after network drops (`connection_retries=-1`).
- `login_qr.py` is a one-time interactive login by QR code (with two-factor password support) that creates the session file.
- JSON logs to stdout (`logsetup.py`); each run logs how many members were tagged.

## Stack

Python 3.12, Telethon, python-dotenv, qrcode, Docker Compose.

## Setup

1. Get `API_ID` and `API_HASH` at https://my.telegram.org (API development tools).
2. Copy `.env.example` to `.env`:

   ```
   API_ID=
   API_HASH=
   SESSION_NAME=data/my_session
   ```

3. Log in once by QR code (Telegram on your phone: Settings -> Devices -> Link Desktop Device):

   ```bash
   pip install -r requirements.txt
   python login_qr.py
   ```

4. Run:

   ```bash
   python main.py
   ```

With Docker: `docker compose up -d --build`, then log in once with `docker exec -it <container> python login_qr.py`. The session is stored in the `allbot_data` volume; if you lose the volume you need to log in again.

The session file gives full access to your Telegram account. Keep it private and never commit it.
