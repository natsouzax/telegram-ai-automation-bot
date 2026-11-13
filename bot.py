"""Telegram automation showcase with opt-in commands and optional scheduled tips."""

import logging
from datetime import datetime, time

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import load_config
from content import generate_tip
from storage import SubscriberStore

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    store: SubscriberStore = context.application.bot_data["store"]
    store.subscribe(update.effective_user.id)
    await update.message.reply_text(
        "Welcome! This demo bot shares educational technology tips. "
        "Use /tip for an example, /help for commands, or /stop to remove your subscription."
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    context.application.bot_data["store"].unsubscribe(update.effective_user.id)
    await update.message.reply_text("Subscription removed. Your saved ID has been deleted.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Commands: /start · /tip · /stop · /help")


async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    config = context.application.bot_data["config"]
    try:
        text = await generate_tip(config.openai_key, config.model, datetime.now(config.timezone).weekday())
    except Exception:
        logging.exception("Tip generation failed")
        await update.message.reply_text("Tip generation is temporarily unavailable.")
        return
    await update.message.reply_text(text)


async def scheduled_tip(context: ContextTypes.DEFAULT_TYPE) -> None:
    config = context.application.bot_data["config"]
    try:
        text = await generate_tip(config.openai_key, config.model, datetime.now(config.timezone).weekday())
        await context.bot.send_message(chat_id=config.target_chat_id, text=text)
    except Exception:
        logging.exception("Scheduled tip failed")


def main() -> None:
    config = load_config()
    store = SubscriberStore(config.database_path)
    app = ApplicationBuilder().token(config.token).build()
    app.bot_data.update(config=config, store=store)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("tip", tip))

    if config.scheduled_posts:
        if not app.job_queue:
            raise RuntimeError("Install python-telegram-bot[job-queue] to enable scheduling")
        app.job_queue.run_daily(scheduled_tip, time=time(hour=9, tzinfo=config.timezone))

    try:
        app.run_polling()
    finally:
        store.close()


if __name__ == "__main__":
    main()
