# Telegram AI Automation Bot

An open-source, anonymized portfolio showcase inspired by a Telegram automation solution I developed for a company. This is an independently rewritten demonstration, **not the original client deployment**. No client-specific code, branding, business information, contact details, or production data are included.

## Features

- Telegram commands: `/start`, `/tip`, `/stop`, `/help`
- AI-generated educational technology tips via the OpenAI API
- Useful fallback tips when no OpenAI key is configured
- Optional daily scheduled messages to a configured Telegram chat
- Lightweight SQLite subscriber persistence, created locally at runtime
- Environment-based configuration; no hard-coded chat IDs or tokens

## Stack

Python · python-telegram-bot · OpenAI API · SQLite · python-dotenv

## Quick start

Requires Python 3.10+ and a Telegram bot token from [@BotFather](https://t.me/BotFather).

```bash
git clone https://github.com/natsouzax/telegram-ai-automation-bot.git
cd telegram-ai-automation-bot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # On Windows, copy the file manually
```

Set `TELEGRAM_BOT_TOKEN` in `.env`, then run:

```bash
python bot.py
```

To use AI-generated tips, set `OPENAI_API_KEY`. Otherwise, `/tip` works with a local demonstration message.

To enable a daily post at 09:00 in the configured time zone, set `ENABLE_SCHEDULED_POSTS=true` and a numeric `TELEGRAM_TARGET_CHAT_ID`. Scheduled posts are disabled by default. Only configure a destination you control or have permission to post to.

## Project structure

| File | Purpose |
| --- | --- |
| `bot.py` | Telegram handlers and scheduling |
| `config.py` | Environment-based settings |
| `content.py` | AI-based and fallback content generation |
| `storage.py` | Local SQLite subscriber records |
| `.env.example` | Safe configuration template |

## Privacy and scope

This repository contains demonstration logic and placeholder configuration only. It does not contain real Telegram user records, proprietary commercial content, credentials, or client screenshots. Runtime databases and `.env` files are excluded from Git. Never commit production data or secrets.

The code is provided as a technical portfolio example. It is not affiliated with or endorsed by the original client.

## Tests

Run `python -m unittest discover -s tests` from the project directory.
