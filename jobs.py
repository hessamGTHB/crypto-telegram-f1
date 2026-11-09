"""
The hourly auto-posting job plus helpers to (re)schedule it.
"""
from __future__ import annotations

import logging

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import Application

import config
import prices
import storage
from formatter import build_price_post

log = logging.getLogger(__name__)

JOB_NAME = "price_post"


async def send_price_post(bot: Bot) -> tuple[bool, str | None]:
    """
    Fetch fresh prices and publish the post to the configured channel.

    Returns (True, None) on success, (False, reason) otherwise.
    """
    state = storage.get_state()
    channel = state.get("channel")
    coins = state.get("coins") or []
    lang = state.get("language", config.DEFAULT_LANGUAGE)

    if not channel:
        return False, "no channel set (use /channel)"
    if not coins:
        return False, "coin list is empty (use /addcoin)"

    try:
        markets = await prices.fetch_markets(coins)
    except prices.PriceFetchError as exc:
        return False, f"CoinGecko: {exc}"

    # Global market cap is a nice-to-have; ignore failures.
    total_cap = cap_change = None
    try:
        glob = await prices.fetch_global()
        total_cap = (glob.get("total_market_cap") or {}).get("usd")
        cap_change = glob.get("market_cap_change_percentage_24h_usd")
    except Exception:  # noqa: BLE001 - never fail the post because of this
        pass

    text = build_price_post(markets, lang, total_cap, cap_change)

    try:
        await bot.send_message(
            chat_id=channel,
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except TelegramError as exc:
        return False, f"Telegram: {exc}"
    return True, None


async def notify_admins(bot: Bot, text: str) -> None:
    """Best-effort DM to every configured admin id."""
    for admin_id in config.ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except TelegramError:
            pass


async def price_post_job(context) -> None:
    """JobQueue callback: post prices and report failures to the admins."""
    ok, reason = await send_price_post(context.bot)
    channel = storage.get_state().get("channel")
    if ok:
        log.info("Price post sent to %s", channel)
        return
    log.warning("Price post failed: %s", reason)
    if config.ADMIN_IDS:
        await notify_admins(
            context.bot,
            "⚠️ قیمت‌ها به کانال ارسال نشدند.\nدلیل: " + (reason or "unknown"),
        )


def schedule_post_job(application: Application, minutes: int) -> None:
    """(Re)create the repeating auto-post job."""
    minutes = max(10, min(1440, int(minutes)))
    application.job_queue.run_repeating(
        price_post_job,
        interval=minutes * 60,
        first=25,  # quick first post so the admin sees it working
        name=JOB_NAME,
    )
    log.info("Auto-post scheduled every %d minute(s)", minutes)


def reschedule(application: Application, minutes: int) -> None:
    """Change the interval of the running job (used by /interval)."""
    for job in application.job_queue.get_jobs_by_name(JOB_NAME):
        job.schedule_removal()
    schedule_post_job(application, minutes)
