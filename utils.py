"""
Formatting helpers: numbers, percentages, market caps and localized dates
(including the Jalali/Persian calendar used for `fa`).
"""
from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import config

# ---------------------------------------------------------------------------
# Digits / numbers
# ---------------------------------------------------------------------------

_FA_TABLE = str.maketrans("0123456789,.%", "۰۱۲۳۴۵۶۷۸۹٬٫٪")

_ASCII_DIGIT_TABLE = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def localize_digits(text: str, lang: str) -> str:
    """Convert Latin digits/punctuation to Persian variants for `fa`."""
    if lang == "fa":
        return text.translate(_FA_TABLE)
    return text


def to_ascii_digits(text: str) -> str:
    """Convert Persian/Arabic digits back to ASCII (e.g. for /interval ۶۰)."""
    return (text or "").translate(_ASCII_DIGIT_TABLE)


def format_price(value, lang: str = "en") -> str:
    """Format a USD price with sensible precision per magnitude."""
    if value is None:
        return "—"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "—"

    if v >= 1000:
        s = f"{v:,.2f}"
    elif v >= 1:
        s = f"{v:,.2f}"
    elif v >= 0.01:
        s = f"{v:.4f}"
    else:
        s = f"{v:.8f}".rstrip("0").rstrip(".")
        if s in ("", "0"):
            s = "0"
    return "$" + localize_digits(s, lang)


def format_pct(pct, lang: str = "en") -> str:
    """Format a 24h change percentage with explicit sign."""
    if pct is None:
        return "—"
    try:
        v = float(pct)
    except (TypeError, ValueError):
        return "—"
    sign = "+" if v >= 0 else "-"
    return localize_digits(f"{sign}{abs(v):.2f}%", lang)


_CAP_SCALES = {
    "fa": ((1e12, "تریلیون"), (1e9, "میلیارد"), (1e6, "میلیون")),
    "zh": ((1e12, "万亿"), (1e9, "十亿"), (1e6, "百万")),
    "ja": ((1e12, "兆"), (1e9, "十億"), (1e6, "百万")),
    "ko": ((1e12, "조"), (1e9, "십억"), (1e6, "백만")),
}


def format_cap(value, lang: str = "en") -> str:
    """Format a total-market-cap style number in the target language."""
    if value is None:
        return "—"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "—"

    if lang in _CAP_SCALES:
        suffix = {"fa": " دلار", "zh": "美元", "ja": "ドル", "ko": " 달러"}[lang]
        sep = " " if lang == "fa" else ""
        for div, label in _CAP_SCALES[lang]:
            if v >= div:
                return localize_digits(f"{v / div:.2f}", lang) + sep + label + suffix
        return localize_digits(f"{v:,.0f}", lang) + suffix

    for div, sym in ((1e12, "T"), (1e9, "B"), (1e6, "M")):
        if v >= div:
            return f"${v / div:.2f}{sym}"
    return f"${v:,.0f}"


# ---------------------------------------------------------------------------
# Calendars / dates
# ---------------------------------------------------------------------------

def gregorian_to_jalali(gy: int, gm: int, gd: int) -> tuple[int, int, int]:
    """Convert a Gregorian date to the Jalali (Persian) calendar."""
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    gy2 = gy - 1600
    gm2 = gm - 1
    gd2 = gd - 1

    g_day_no = 365 * gy2 + (gy2 + 3) // 4 - (gy2 + 99) // 100 + (gy2 + 399) // 400
    g_day_no += g_d_m[gm2]
    if gm2 > 1 and ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        g_day_no += 1
    g_day_no += gd2

    j_day_no = g_day_no - 79
    j_np = j_day_no // 12053
    j_day_no %= 12053
    jy = 979 + 33 * j_np + 4 * (j_day_no // 1461)
    j_day_no %= 1461
    if j_day_no >= 366:
        jy += (j_day_no - 1) // 365
        j_day_no = (j_day_no - 1) % 365

    if j_day_no < 186:
        jm = 1 + j_day_no // 31
        jd = 1 + j_day_no % 31
    else:
        jm = 7 + (j_day_no - 186) // 30
        jd = 1 + (j_day_no - 186) % 30
    return jy, jm, jd


JALALI_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",
]

WEEKDAYS = {
    # Monday .. Sunday
    "fa": ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "zh": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"],
    "ja": ["月", "火", "水", "木", "金", "土", "日"],
    "ko": ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"],
    "hi": ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"],
}

_MONTHS_EN = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

_MONTHS_HI = [
    "जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून",
    "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर",
]


def now_local() -> datetime:
    """Current time in the configured timezone (UTC fallback)."""
    try:
        tz = ZoneInfo(config.TIMEZONE)
    except Exception:
        tz = timezone.utc
    return datetime.now(tz)


def format_datetime(lang: str) -> str:
    """Human readable 'now' string per language, e.g. the post timestamp."""
    dt = now_local()
    offset = dt.strftime("%z")
    if offset and len(offset) == 5:
        offset = f"UTC{offset[:3]}:{offset[3:]}"
    wd = WEEKDAYS.get(lang, WEEKDAYS["en"])[dt.weekday()]
    hhmm = f"{dt:%H:%M}"

    if lang == "fa":
        jy, jm, jd = gregorian_to_jalali(dt.year, dt.month, dt.day)
        base = f"{wd} {jd} {JALALI_MONTHS[jm - 1]} {jy} · {hhmm}"
        return localize_digits(base, "fa") + f" ({localize_digits(offset, 'fa')})"
    if lang == "en":
        return f"{wd}, {_MONTHS_EN[dt.month - 1]} {dt.day}, {dt.year} · {hhmm} ({offset})"
    if lang == "zh":
        return f"{dt.year}年{dt.month}月{dt.day}日 {wd} · {hhmm} ({offset})"
    if lang == "ja":
        return f"{dt.year}年{dt.month}月{dt.day}日（{wd}）{hhmm} ({offset})"
    if lang == "ko":
        return f"{dt.year}년 {dt.month}월 {dt.day}일 ({wd}) {hhmm} ({offset})"
    if lang == "hi":
        return f"{dt.day} {_MONTHS_HI[dt.month - 1]} {dt.year}, {wd} · {hhmm} ({offset})"
    return f"{wd}, {_MONTHS_EN[dt.month - 1]} {dt.day}, {dt.year} · {hhmm} ({offset})"
