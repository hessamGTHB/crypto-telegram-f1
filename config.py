"""
Configuration for the crypto channel bot.

All settings are read from environment variables or an optional `.env` file
located next to this module. See `.env.example` for a documented template.
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    # Load .env if python-dotenv is installed; otherwise fall back to env vars.
    load_dotenv()
except ImportError:  # pragma: no cover - dotenv is optional
    pass

BASE_DIR = Path(__file__).resolve().parent

SUPPORTED_LANGUAGES = ("fa", "en", "zh", "ja", "ko", "hi")


def _int_env(name: str, default: int, lo: int | None = None, hi: int | None = None) -> int:
    """Read an integer env var with optional clamping."""
    raw = os.getenv(name, "")
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        value = default
    if lo is not None:
        value = max(lo, value)
    if hi is not None:
        value = min(hi, value)
    return value


# --- Telegram ---------------------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Comma separated numeric Telegram user ids. Persian/Arabic commas are also
# accepted so "123,456" and "123،456" both work.
_raw_admins = os.getenv("ADMIN_IDS", "").replace("،", ",").replace("؛", ",")
ADMIN_IDS = frozenset(
    int(part.strip())
    for part in _raw_admins.split(",")
    if part.strip().lstrip("-").isdigit()
)

# --- Defaults for the mutable state (see storage.py) ------------------------
DEFAULT_CHANNEL = os.getenv("CHANNEL_ID", "").strip()  # "@name" or "-100..."
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "fa").strip().lower()
if DEFAULT_LANGUAGE not in SUPPORTED_LANGUAGES:
    DEFAULT_LANGUAGE = "fa"

# Auto-posting interval in minutes. CoinGecko's free tier is rate limited,
# anything below 10 minutes is discouraged.
DEFAULT_INTERVAL = _int_env("POST_INTERVAL_MINUTES", 60, 10, 1440)

# --- Price source -----------------------------------------------------------
# Optional CoinGecko demo/pro API key. If set it is sent as `x-cg-demo-api-key`.
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "").strip()

# --- Presentation -----------------------------------------------------------
TIMEZONE = os.getenv("TIMEZONE", "Asia/Tehran").strip() or "UTC"
FOOTER_TEXT = os.getenv("FOOTER_TEXT", "").strip()  # e.g. "@your_channel"
MAX_COINS = _int_env("MAX_COINS", 15, 1, 30)

# --- Storage ----------------------------------------------------------------
_data_dir_raw = os.getenv("DATA_DIR", "data")
_data_path = Path(_data_dir_raw)
DATA_DIR = _data_path if _data_path.is_absolute() else BASE_DIR / _data_path
