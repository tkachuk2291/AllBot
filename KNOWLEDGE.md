# AllBot — база знаний

Юзербот на Telethon (работает от аккаунта пользователя, не бот-токен). Команда `.all`, отправленная
самим владельцем в любом чате, удаляется и заменяется упоминаниями всех участников пачками по 5 раз в секунду.

## Устройство
- `main.py` — клиент `TelegramClient(session, API_ID, API_HASH, connection_retries=-1, retry_delay=10)`:
  бесконечно переподключается при обрывах сети.
- `login_qr.py` — разовый вход по QR (интерактивно, через `docker exec -it`), создаёт файл сессии.
- Сессия хранится в томе `allbot_data:/data` (`SESSION_NAME`). Потеря тома = заново логиниться по QR.

## Деплой
- Стек Portainer `all_bot`, файлы: `/var/lib/docker/volumes/portainer_data/_data/compose/2`, секреты в `stack.env` (API_ID, API_HASH).
- Dockerfile копирует только `*.py` из корня.

## Логи
- После `.all` пишется `event: "stat", stat: "tag_all", members: N` — админ-бот считает запуски и отмеченных людей.
- JSON (`logsetup.py`), bot=all-bot. Логи telethon (подключения) идут на уровне INFO.
- Ошибки в обработчиках Telethon логирует сам (`telethon.client.updates`), в контексте есть `chat_id`.

## Инциденты
- До 2026-10-18 на сервере была непушнутая правка `connection_retries=-1` — занесена в git.
