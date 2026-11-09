"""
Crypto Channel Bot — entry point.

Posts live cryptocurrency prices (CoinGecko) to a Telegram channel on a
schedule, with a 6-language interface (fa / en / zh / ja / ko / hi).

Run:  python bot.py
"""
from __future__ import annotations

import logging
import sys

from telegram import BotCommand, Update
from telegram.ext import Application, ApplicationBuilder

import config
import handlers
import jobs
import storage



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("bot")

COMMANDS = [
    BotCommand("start", "Start / شروع"),
    BotCommand("help", "Help / راهنما"),
    BotCommand("lang", "Language / زبان"),
    BotCommand("post", "Post prices now (admin)"),
    BotCommand("coins", "Coin list (admin)"),
    BotCommand("addcoin", "Add a coin (admin)"),
    BotCommand("delcoin", "Remove a coin (admin)"),
    BotCommand("channel", "Set channel (admin)"),
    BotCommand("interval", "Post interval (admin)"),
    BotCommand("status", "Bot status (admin)"),
]


async def post_init(app: Application) -> None:
    """Runs once after the bot is up: set the command menu and log status."""
    try:
        await app.bot.set_my_commands(COMMANDS)
    except Exception as exc:  # noqa: BLE001 - menu is nice-to-have
        log.warning("Could not set command menu: %s", exc)

    me = await app.bot.get_me()
    state = storage.get_state()
    log.info(
        "Bot is live as @%s | post language=%s | coins=%d | interval=%d min | admins=%s",
        me.username,
        state.get("language"),
        len(state.get("coins") or []),
        state.get("interval_minutes"),
        sorted(config.ADMIN_IDS) or "(none set — private chats are treated as admin)",
    )
    if not config.ADMIN_IDS:
        log.warning(
            "ADMIN_IDS is empty! Anyone in a private chat can manage the bot. "
            "Set your numeric id in .env as soon as possible."
        )
    if state.get("channel"):
        try:
            chat = await app.bot.get_chat(state["channel"])
            log.info("Target channel OK: %s", getattr(chat, "title", state["channel"]))
        except Exception as exc:  # noqa: BLE001
            log.warning("Configured channel is not reachable yet: %s", exc)


def main() -> None:
    if not config.BOT_TOKEN or ":" not in config.BOT_TOKEN:
        print(
            "خطا: توکن ربات تنظیم نشده است.\n"
            "فایل `.env.example` را به `.env` تغییر نام دهید و مقدار BOT_TOKEN "
            "را از @BotFather داخل آن قرار دهید."
        )
        sys.exit(1)

    storage.init()

    app = (
        ApplicationBuilder()
        .token(config.BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    handlers.register(app)
    jobs.schedule_post_job(app, storage.get_state()["interval_minutes"])

    log.info("Starting polling…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
