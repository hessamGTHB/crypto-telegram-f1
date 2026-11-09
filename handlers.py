"""
All Telegram handlers: public commands (/start, /help, /lang) and the
admin-only management commands (/post, /coins, /addcoin, /delcoin,
/channel, /interval, /status).
"""
from __future__ import annotations

import html
import logging

from telegram import Update
from telegram.constants import ChatType, ParseMode
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

import config
import i18n
import jobs
import prices
import storage
import utils
from formatter import build_price_post, coin_choice_keyboard, display_coin, language_keyboard
from i18n import t

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _lang(update: Update) -> str:
    """UI language of the effective user (falls back to the default)."""
    user = update.effective_user
    state = storage.get_state()
    if user is not None:
        code = state.get("user_languages", {}).get(str(user.id))
        if code in config.SUPPORTED_LANGUAGES:
            return code
    return state.get("language", config.DEFAULT_LANGUAGE)


def _is_admin(update: Update) -> bool:
    """
    Admins are the numeric ids from ADMIN_IDS.

    If ADMIN_IDS is empty, anyone chatting with the bot in private is treated
    as admin (handy for the first setup) — set ADMIN_IDS before using the bot
    in public groups.
    """
    user = update.effective_user
    if user is None:
        return False
    if user.id in config.ADMIN_IDS:
        return True
    if config.ADMIN_IDS:
        return False
    chat = update.effective_chat
    return bool(chat) and chat.type == ChatType.PRIVATE


def _user_display_name(update: Update) -> str:
    user = update.effective_user
    if user is None:
        return ""
    return html.escape(user.first_name or user.full_name or "")


# ---------------------------------------------------------------------------
# Public commands
# ---------------------------------------------------------------------------

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    name = _user_display_name(update) or t(lang, "status_not_set")
    text = t(lang, "welcome", name=name, choose=t(lang, "choose_language"))
    await update.effective_message.reply_text(
        text,
        reply_markup=language_keyboard(current=lang),
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    key = "help_admin" if _is_admin(update) else "help_user"
    await update.effective_message.reply_text(t(lang, key))


async def cmd_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    await update.effective_message.reply_text(
        t(lang, "choose_language"),
        reply_markup=language_keyboard(current=lang),
    )


async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Language button pressed. Admins also change the channel post language."""
    query = update.callback_query
    if query is None:
        return
    await query.answer()

    user = update.effective_user
    code = (query.data or "").split(":", 1)[1]
    if code not in config.SUPPORTED_LANGUAGES:
        return

    state = storage.get_state()
    if user is not None:
        state.setdefault("user_languages", {})[str(user.id)] = code
    storage.save()

    label = i18n.LANGUAGES.get(code, code)
    text = t(code, "lang_changed", lang=label)
    if _is_admin(update):
        state["language"] = code
        storage.save()
        text += "\n" + t(code, "channel_lang_updated", lang=label)

    await query.edit_message_text(
        text,
        reply_markup=language_keyboard(current=code),
    )


# ---------------------------------------------------------------------------
# Admin: posting
# ---------------------------------------------------------------------------

async def cmd_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not _is_admin(update):
        await update.effective_message.reply_text(t(lang, "msg_only_admin"))
        return

    state = storage.get_state()
    if not state.get("channel"):
        await update.effective_message.reply_text(t(lang, "msg_no_channel"))
        return

    ok, reason = await jobs.send_price_post(context.bot)
    if ok:
        await update.effective_message.reply_text(
            t(lang, "msg_posted", channel=state["channel"])
        )
    else:
        await update.effective_message.reply_text(
            t(lang, "msg_post_failed", error=reason or "?")
        )


# ---------------------------------------------------------------------------
# Admin: coin list management
# ---------------------------------------------------------------------------

def _add_coin(cid: str) -> str:
    """Add a coin id to the list. Returns 'ok' | 'dup' | 'max'."""
    state = storage.get_state()
    if cid in state["coins"]:
        return "dup"
    if len(state["coins"]) >= config.MAX_COINS:
        return "max"
    state["coins"].append(cid)
    storage.save()
    return "ok"


def _remove_coin(cid: str) -> bool:
    state = storage.get_state()
    if cid in state["coins"]:
        state["coins"].remove(cid)
        storage.save()
        return True
    return False


async def cmd_coins(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not _is_admin(update):
        await update.effective_message.reply_text(t(lang, "msg_only_admin"))
        return

    coins = storage.get_state().get("coins") or []
    if not coins:
        await update.effective_message.reply_text(t(lang, "msg_empty_list"))
        return

    lines = [t(lang, "current_coins", count=utils.localize_digits(str(len(coins)), lang))]
    for idx, cid in enumerate(coins, 1):
        lines.append(f"{idx}. {display_coin(cid, lang)}")
        lines.append(f"    <code>/delcoin {html.escape(cid)}</code>")
    await update.effective_message.reply_text(
        "\n".join(lines),
        parse_mode=ParseMode.HTML,
    )


async def cmd_addcoin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not _is_admin(update):
        await update.effective_message.reply_text(t(lang, "msg_only_admin"))
        return

    query = " ".join(context.args or []).strip()
    if not query:
        await update.effective_message.reply_text(t(lang, "msg_usage_addcoin"))
        return

    try:
        kind, candidates = await prices.resolve_coin(query)
    except prices.PriceFetchError as exc:
        log.warning("addcoin lookup failed: %s", exc)
        await update.effective_message.reply_text(
            t(lang, "msg_post_failed", error=f"CoinGecko: {exc}")
        )
        return

    if kind == "none" or not candidates:
        await update.effective_message.reply_text(t(lang, "msg_coin_not_found", query=query))
        return

    coin = candidates[0]
    if kind == "exact":
        status = _add_coin(coin["id"])
        if status == "dup":
            await update.effective_message.reply_text(t(lang, "msg_already_added"))
        elif status == "max":
            await update.effective_message.reply_text(
                t(lang, "max_coins_reached", max=config.MAX_COINS)
            )
        else:
            await update.effective_message.reply_text(
                t(
                    lang,
                    "msg_coin_added",
                    coin=display_coin(
                        coin["id"], lang, name_raw=coin.get("name"), symbol=coin.get("symbol")
                    ),
                )
            )
        return

    fresh = [c for c in candidates if c.get("id") not in storage.get_state()["coins"]]
    if not fresh:
        await update.effective_message.reply_text(t(lang, "msg_already_added"))
        return

    await update.effective_message.reply_text(
        t(lang, "pick_coin"),
        reply_markup=coin_choice_keyboard(fresh, prefix="add"),
    )


async def add_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return
    lang = _lang(update)
    if not _is_admin(update):
        await query.answer(t(lang, "msg_only_admin"), show_alert=True)
        return
    await query.answer()

    cid = (query.data or "").split(":", 1)[1]
    coin = {"id": cid}
    status = _add_coin(cid)
    if status == "dup":
        await query.edit_message_text(t(lang, "msg_already_added"))
    elif status == "max":
        await query.edit_message_text(t(lang, "max_coins_reached", max=config.MAX_COINS))
    else:
        await query.edit_message_text(
            t(lang, "msg_coin_added", coin=display_coin(cid, lang, name_raw=coin.get("name")))
        )


async def cmd_delcoin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not _is_admin(update):
        await update.effective_message.reply_text(t(lang, "msg_only_admin"))
        return

    query = " ".join(context.args or []).strip()
    if not query:
        await update.effective_message.reply_text(t(lang, "msg_usage_delcoin"))
        return

    coins = storage.get_state().get("coins") or []

    # 1) direct id match, no API call needed
    direct = query.strip().lower().replace(" ", "-")
    if direct in coins:
        _remove_coin(direct)
        await update.effective_message.reply_text(
            t(lang, "msg_coin_removed", coin=display_coin(direct, lang))
        )
        return

    # 2) otherwise resolve the name/ticker through CoinGecko
    try:
        kind, candidates = await prices.resolve_coin(query)
    except prices.PriceFetchError as exc:
        log.warning("delcoin lookup failed: %s", exc)
        await update.effective_message.reply_text(
            t(lang, "msg_post_failed", error=f"CoinGecko: {exc}")
        )
        return

    if kind == "exact" and candidates:
        cid = candidates[0]["id"]
        if _remove_coin(cid):
            await update.effective_message.reply_text(
                t(lang, "msg_coin_removed", coin=display_coin(cid, lang))
            )
        else:
            await update.effective_message.reply_text(t(lang, "msg_not_in_list", query=query))
        return

    in_list = [c for c in candidates if c.get("id") in coins]
    if len(in_list) == 1:
        cid = in_list[0]["id"]
        _remove_coin(cid)
        await update.effective_message.reply_text(
            t(lang, "msg_coin_removed", coin=display_coin(cid, lang))
        )
    elif not in_list:
        await update.effective_message.reply_text(t(lang, "msg_not_in_list", query=query))
    else:
        await update.effective_message.reply_text(
            t(lang, "pick_coin"),
            reply_markup=coin_choice_keyboard(in_list, prefix="del"),
        )


async def del_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return
    lang = _lang(update)
    if not _is_admin(update):
        await query.answer(t(lang, "msg_only_admin"), show_alert=True)
        return
    await query.answer()

    cid = (query.data or "").split(":", 1)[1]
    if _remove_coin(cid):
        await query.edit_message_text(t(lang, "msg_coin_removed", coin=display_coin(cid, lang)))
    else:
        await query.edit_message_text(t(lang, "msg_not_in_list", query=cid))


# ---------------------------------------------------------------------------
# Admin: channel & interval
# ---------------------------------------------------------------------------

async def cmd_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not _is_admin(update):
        await update.effective_message.reply_text(t(lang, "msg_only_admin"))
        return

    arg = (context.args or [""])[0].strip()
    if not arg:
        await update.effective_message.reply_text(t(lang, "msg_usage_channel"))
        return

    target = arg if arg.startswith("@") or arg.startswith("-") else f"@{arg}"

    try:
        chat = await context.bot.get_chat(target)
    except TelegramError as exc:
        await update.effective_message.reply_text(
            t(lang, "msg_channel_fail", error=str(exc))
        )
        return

    # Probe: send + immediately delete a test message to verify write access.
    try:
        probe = await context.bot.send_message(target, "…")
        await probe.delete()
    except TelegramError as exc:
        await update.effective_message.reply_text(
            t(lang, "msg_channel_fail", error=str(exc))
        )
        return

    state = storage.get_state()
    state["channel"] = target
    storage.save()

    label = html.escape(str(getattr(chat, "title", None) or target))
    await update.effective_message.reply_text(t(lang, "msg_channel_set", channel=label))


async def cmd_interval(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not _is_admin(update):
        await update.effective_message.reply_text(t(lang, "msg_only_admin"))
        return

    raw = (context.args or [""])[0].strip()
    try:
        minutes = int(utils.to_ascii_digits(raw))
    except ValueError:
        await update.effective_message.reply_text(t(lang, "msg_usage_interval"))
        return

    if not 10 <= minutes <= 1440:
        await update.effective_message.reply_text(t(lang, "msg_usage_interval"))
        return

    state = storage.get_state()
    state["interval_minutes"] = minutes
    storage.save()
    jobs.reschedule(context.application, minutes)

    await update.effective_message.reply_text(
        t(lang, "msg_interval_set", minutes=utils.localize_digits(str(minutes), lang))
    )


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not _is_admin(update):
        await update.effective_message.reply_text(t(lang, "msg_only_admin"))
        return

    state = storage.get_state()
    channel_value = state.get("channel") or t(lang, "status_not_set")
    lang_value = i18n.LANGUAGES.get(state.get("language", ""), state.get("language", "?"))

    lines = [
        t(lang, "status_title"),
        t(lang, "status_channel", value=channel_value),
        t(lang, "status_language", value=lang_value),
        t(
            lang,
            "status_interval",
            value=utils.localize_digits(str(state.get("interval_minutes", "?")), lang),
        ),
        t(
            lang,
            "status_coins",
            count=utils.localize_digits(str(len(state.get("coins") or [])), lang),
        ),
    ]
    await update.effective_message.reply_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Error handler & registration
# ---------------------------------------------------------------------------

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.error("Update error", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                t(_lang(update), "error_generic")
            )
        except TelegramError:
            pass


def register(app: Application) -> None:
    """Attach every handler to the application."""
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("lang", cmd_lang))
    app.add_handler(CommandHandler("post", cmd_post))
    app.add_handler(CommandHandler("coins", cmd_coins))
    app.add_handler(CommandHandler("addcoin", cmd_addcoin))
    app.add_handler(CommandHandler("delcoin", cmd_delcoin))
    app.add_handler(CommandHandler("channel", cmd_channel))
    app.add_handler(CommandHandler("interval", cmd_interval))
    app.add_handler(CommandHandler("status", cmd_status))

    app.add_handler(CallbackQueryHandler(lang_callback, pattern=r"^lang:"))
    app.add_handler(CallbackQueryHandler(add_callback, pattern=r"^add:"))
    app.add_handler(CallbackQueryHandler(del_callback, pattern=r"^del:"))

    app.add_error_handler(error_handler)
