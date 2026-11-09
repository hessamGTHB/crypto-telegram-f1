"""
Tiny JSON persistence layer.

Bot settings (channel, coin list, language, interval, per-user languages)
are stored in `data/state.json` so they survive restarts without a database.
"""
import json
import logging
from pathlib import Path
from typing import Any

import config

log = logging.getLogger(__name__)

DEFAULTS: dict[str, Any] = {
    "channel": config.DEFAULT_CHANNEL or None,
    "coins": [
        "bitcoin",
        "ethereum",
        "binancecoin",
        "solana",
        "ripple",
        "dogecoin",
    ],
    "language": config.DEFAULT_LANGUAGE,
    "interval_minutes": config.DEFAULT_INTERVAL,
    "user_languages": {},
}

_PATH = Path(config.DATA_DIR) / "state.json"
_state: dict[str, Any] | None = None


def _normalize(raw: dict[str, Any]) -> dict[str, Any]:
    """Merge stored data over defaults and sanitize types."""
    state = {**DEFAULTS, **{k: v for k, v in raw.items() if k in DEFAULTS}}

    if not isinstance(state.get("coins"), list):
        state["coins"] = list(DEFAULTS["coins"])
    state["coins"] = [str(c) for c in state["coins"] if str(c).strip()]

    if state.get("language") not in config.SUPPORTED_LANGUAGES:
        state["language"] = DEFAULTS["language"]

    try:
        state["interval_minutes"] = max(10, min(1440, int(state["interval_minutes"])))
    except (TypeError, ValueError):
        state["interval_minutes"] = DEFAULTS["interval_minutes"]

    if not isinstance(state.get("user_languages"), dict):
        state["user_languages"] = {}

    channel = state.get("channel")
    state["channel"] = str(channel).strip() if channel and str(channel).strip() else None
    return state


def load_state() -> dict[str, Any]:
    """Load state.json, falling back to defaults when missing or broken."""
    try:
        raw = json.loads(_PATH.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("state.json must contain an object")
        state = _normalize(raw)
    except FileNotFoundError:
        state = {**DEFAULTS, "coins": list(DEFAULTS["coins"]), "user_languages": {}}
        log.info("No state file found, using defaults")
    except (json.JSONDecodeError, ValueError, OSError) as exc:
        log.warning("Could not read state file (%s), using defaults", exc)
        state = {**DEFAULTS, "coins": list(DEFAULTS["coins"]), "user_languages": {}}
    return state


def init(state: dict[str, Any] | None = None) -> dict[str, Any]:
    """Initialize the in-memory state (called once at startup)."""
    global _state
    _state = state if state is not None else load_state()
    return _state


def get_state() -> dict[str, Any]:
    """Access the current state, loading it lazily if needed."""
    if _state is None:
        init()
    assert _state is not None
    return _state


def save() -> None:
    """Persist the current state to disk (atomic write)."""
    _PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = _PATH.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(get_state(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    tmp.replace(_PATH)
