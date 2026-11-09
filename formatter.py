"""
Message builders: the channel price post and inline keyboards.
"""
from __future__ import annotations

import html

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import config
import i18n
import utils

SEP = "━━━━━━━━━━━━━━━━━━"


def language_keyboard(current: str | None = None, prefix: str = "lang") -> InlineKeyboardMarkup:
    """Two-column language picker (6 languages)."""
    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for code, label in i18n.LANGUAGES.items():
        mark = " ●" if code == current else ""
        row.append(InlineKeyboardButton(f"{label}{mark}", callback_data=f"{prefix}:{code}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def coin_choice_keyboard(
    candidates: list[dict],
    prefix: str = "add",
) -> InlineKeyboardMarkup:
    """One button per search result so the admin can pick a coin."""
    rows: list[list[InlineKeyboardButton]] = []
    for coin in candidates:
        cid = str(coin.get("id") or "").strip()
        if not cid:
            continue
        symbol = (coin.get("symbol") or "").upper()
        name = coin.get("name") or cid
        rank = coin.get("market_cap_rank")
        label = f"{name} ({symbol})" if symbol else name
        if isinstance(rank, int) and rank > 0:
            label = f"{label} · #{rank}"
        rows.append([InlineKeyboardButton(label[:64], callback_data=f"{prefix}:{cid}")])
    return InlineKeyboardMarkup(rows)


def display_coin(cid: str, lang: str, name_raw: str | None = None, symbol: str | None = None) -> str:
    """Nice one-line representation of a coin: '₿ بیت‌کوین (BTC)'."""
    name = i18n.coin_name(cid, lang, fallback=name_raw or cid)
    sym = (symbol or i18n.COIN_SYMBOLS.get(cid, "")).upper()
    emoji = i18n.COIN_EMOJI.get(sym.lower(), "💠")
    return f"{emoji} {name} ({sym})" if sym else f"{emoji} {name}"


def build_price_post(
    markets: list[dict],
    lang: str,
    total_cap=None,
    cap_change=None,
) -> str:
    """
    Build the HTML-formatted channel post:

        📊 Live Crypto Prices
        ━━━━━━━━━━━━━━━━━━
        ₿ Bitcoin · BTC
        💵 $97,450.12   🟢 +2.35%
        ━━━━━━━━━━━━━━━━━━
        ...
        🌍 Total Market Cap: $3.12T  🟢 +1.23%
        🕐 Saturday, November 8, 2025 · 14:00 (UTC+03:30)
        🔗 Data: CoinGecko
    """
    if not markets:
        return i18n.t(lang, "msg_empty_list")

    lines: list[str] = [f"📊 <b>{i18n.t(lang, 'post_title')}</b>", SEP]

    for m in markets:
        if not isinstance(m, dict):
            continue
        cid = str(m.get("id") or "")
        symbol = (m.get("symbol") or "").upper()
        name = i18n.coin_name(cid, lang, fallback=m.get("name") or cid)
        emoji = i18n.COIN_EMOJI.get((m.get("symbol") or "").lower(), "💠")

        title = f"{emoji} <b>{html.escape(name)}</b>"
        if symbol:
            title += f" · {symbol}"
        lines.append(title)

        price = utils.format_price(m.get("current_price"), lang)
        pct = m.get("price_change_percentage_24h")
        icon = "🟢" if (pct is not None and float(pct) >= 0) else "🔴"
        lines.append(f"💵 <b>{price}</b>   {icon} {utils.format_pct(pct, lang)}")
        lines.append(SEP)

    if total_cap is not None:
        cap_line = (
            f"🌍 {i18n.t(lang, 'market_cap_total')}: "
            f"<b>{utils.format_cap(total_cap, lang)}</b>"
        )
        if cap_change is not None:
            icon = "🟢" if float(cap_change) >= 0 else "🔴"
            cap_line += f"  {icon} {utils.format_pct(cap_change, lang)}"
        lines.append(cap_line)

    lines.append(f"🕐 {utils.format_datetime(lang)}")
    lines.append(f"🔗 {i18n.t(lang, 'source')}: CoinGecko")

    if config.FOOTER_TEXT:
        lines.append(html.escape(config.FOOTER_TEXT))

    return "\n".join(lines)
