"""
Async client for the free CoinGecko public API (v3).

Endpoints used:
    /coins/markets  – prices, 24h change and market cap for a list of ids
    /global         – total market cap and its 24h change
    /search         – resolve a user-typed name/ticker to a CoinGecko id

The free API is rate limited (~5-30 req/min depending on load), so every
call retries a few times with backoff on 429/network errors.
"""
from __future__ import annotations

import asyncio
import logging

import httpx

import config

log = logging.getLogger(__name__)

BASE_URL = "https://api.coingecko.com/api/v3"
TIMEOUT = 15.0
RETRIES = 3


class PriceFetchError(Exception):
    """Raised when CoinGecko cannot be reached or answers with an error."""


def _headers() -> dict[str, str]:
    headers = {
        "accept": "application/json",
        "user-agent": "crypto-channel-bot/1.0",
    }
    if config.COINGECKO_API_KEY:
        headers["x-cg-demo-api-key"] = config.COINGECKO_API_KEY
    return headers


async def _get(path: str, params: dict[str, str] | None = None):
    last_error: Exception | None = None
    params = params or {}
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=TIMEOUT) as client:
        for attempt in range(RETRIES):
            try:
                resp = await client.get(path, params=params, headers=_headers())
                if resp.status_code == 429:  # rate limited -> back off
                    await asyncio.sleep(2.0 * (attempt + 1))
                    last_error = PriceFetchError("rate limited (HTTP 429)")
                    continue
                resp.raise_for_status()
                return resp.json()
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                await asyncio.sleep(1.5 * (attempt + 1))
    raise PriceFetchError(str(last_error))


async def fetch_markets(coin_ids: list[str]) -> list[dict]:
    """Price snapshot for the given CoinGecko ids (USD)."""
    ids = ",".join(dict.fromkeys(i.strip() for i in coin_ids if i.strip()))
    if not ids:
        return []
    data = await _get(
        "/coins/markets",
        {
            "vs_currency": "usd",
            "ids": ids,
            "order": "market_cap_desc",
            "per_page": str(max(len(coin_ids), 1)),
            "page": "1",
            "sparkline": "false",
            "price_change_percentage": "24h",
        },
    )
    if not isinstance(data, list):
        raise PriceFetchError("unexpected /coins/markets response")
    # Keep the order requested by the user, not CoinGecko's ordering.
    by_id = {item.get("id"): item for item in data if isinstance(item, dict)}
    ordered = [by_id[cid] for cid in ids.split(",") if cid in by_id]
    missing = [cid for cid in ids.split(",") if cid not in by_id]
    if missing:
        log.warning("No market data for: %s", ", ".join(missing))
    return ordered


async def fetch_global() -> dict:
    """Global market stats (total market cap, 24h change, ...)."""
    data = await _get("/global")
    if not isinstance(data, dict) or not isinstance(data.get("data"), dict):
        raise PriceFetchError("unexpected /global response")
    return data["data"]


async def search_coins(query: str, limit: int = 6) -> list[dict]:
    """Search CoinGecko for coins matching a free-text query."""
    data = await _get("/search", {"query": query.strip()})
    coins = data.get("coins") if isinstance(data, dict) else None
    if not isinstance(coins, list):
        return []
    return coins[:limit]


# /coins/list is a large static catalog; fetch it once per process and cache.
_COIN_LIST_CACHE: list[dict] | None = None


async def _coins_list() -> list[dict]:
    global _COIN_LIST_CACHE
    if _COIN_LIST_CACHE is None:
        data = await _get("/coins/list")
        if not isinstance(data, list):
            raise PriceFetchError("unexpected /coins/list response")
        _COIN_LIST_CACHE = data
    return _COIN_LIST_CACHE


def _norm(value) -> str:
    return (value or "").strip().lower()


async def _fallback_lookup(q: str) -> tuple[str, list[dict]]:
    """
    Backup resolution path used when /search is unavailable or returns
    nothing (CoinGecko sometimes degrades anonymous search on some IPs):

      1. match against the full /coins/list catalog (cached)
      2. try the query directly as a coin id via /coins/markets
    """
    ql = _norm(q).replace(" ", "-")

    # --- 1: catalog match ------------------------------------------------
    try:
        catalog = await _coins_list()
        exact = [c for c in catalog if _norm(c.get("id")) == ql]
        if exact:
            return "exact", [dict(exact[0])]
        symbol_hits = [c for c in catalog if _norm(c.get("symbol")) == ql]
        if symbol_hits:
            # Prefer the coin whose id equals the symbol (the "canonical" one),
            # then the shortest id which is usually the most established.
            symbol_hits.sort(key=lambda c: (_norm(c.get("id")) != ql, len(c.get("id") or "")))
            wrapped = [dict(c) for c in symbol_hits[:6]]
            if len(wrapped) == 1:
                return "exact", wrapped
            return "pick", wrapped
    except PriceFetchError as exc:
        log.warning("coins/list fallback failed: %s", exc)

    # --- 2: treat the query itself as a CoinGecko id ----------------------
    try:
        data = await _get(
            "/coins/markets",
            {
                "vs_currency": "usd",
                "ids": ql,
                "order": "market_cap_desc",
                "per_page": "1",
                "page": "1",
                "sparkline": "false",
                "price_change_percentage": "24h",
            },
        )
        if isinstance(data, list) and data:
            row = data[0]
            return "exact", [{
                "id": row.get("id"),
                "name": row.get("name"),
                "symbol": row.get("symbol"),
                "market_cap_rank": row.get("market_cap_rank"),
            }]
    except PriceFetchError as exc:
        log.warning("direct-id fallback failed: %s", exc)

    return "none", []


async def resolve_coin(query: str) -> tuple[str, list[dict]]:
    """
    Turn user input (id, ticker or name) into a CoinGecko coin.

    Returns:
        ("exact", [coin])       – unambiguous match, safe to add directly
        ("pick", [candidates])  – several candidates, show a picker
        ("none", [])            – nothing found

    Uses /search first and transparently falls back to the /coins/list
    catalog + direct-id lookup when the search API is degraded.
    """
    q = query.strip()
    if not q:
        return "none", []

    try:
        results = await search_coins(q)
    except PriceFetchError as exc:
        log.warning("/search failed (%s), using fallback lookup", exc)
        results = []

    for coin in results:
        if _norm(coin.get("id")) == _norm(q):
            return "exact", [coin]

    symbol_matches = [c for c in results if _norm(c.get("symbol")) == _norm(q)]
    if len(symbol_matches) == 1:
        return "exact", symbol_matches
    if symbol_matches:
        return "pick", symbol_matches[:6]

    if results:
        return "pick", results[:6]

    return await _fallback_lookup(q)
