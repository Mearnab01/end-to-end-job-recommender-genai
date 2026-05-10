"""
Lightweight mem0 wrapper.

Uses the mem0 *platform* (cloud) client so no local vector DB or
sentence-transformers are needed — just a MEM0_API_KEY in secrets/env.

If the key is missing the module degrades gracefully: all functions
return empty results and log a warning rather than crashing.
"""

import os
from utils.logger import get_logger

logger = get_logger("memory")

# Fix for SSL issues sometimes seen on Windows
if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]


def _api_key() -> str:
    """Read MEM0_API_KEY from Streamlit secrets or environment."""
    try:
        import streamlit as st
        return st.secrets.get("MEM0_API_KEY", "")
    except Exception:
        return os.getenv("MEM0_API_KEY", "")


def _client():
    """Return a MemoryClient or None if the key is absent."""
    key = _api_key()
    if not key:
        logger.warning("MEM0_API_KEY not set — memory features disabled")
        return None
    try:
        from mem0 import MemoryClient
        return MemoryClient(api_key=key)
    except Exception as exc:
        logger.warning("mem0 client init failed: %s", exc)
        return None


# =========================================
# PUBLIC HELPERS
# =========================================

def save_search(user_id: str, keywords: str) -> None:
    """Store the user's latest search keywords in mem0."""
    client = _client()
    if not client:
        return
    try:
        client.add(
            f"Job search: {keywords}",
            user_id=str(user_id),
        )
        logger.info("Memory saved | user=%s | %.40s", user_id, keywords)
    except Exception as exc:
        logger.warning("Memory save failed: %s", exc)


def get_preferences(user_id: str) -> list[str]:
    """
    Returns a list of remembered search strings for this user.
    Returns [] if mem0 is unavailable.
    """
    client = _client()
    if not client:
        return []
    try:
        raw = client.get_all(user_id=str(user_id))
        # API returns a list or a dict with a 'results' key
        items = raw.get("results", raw) if isinstance(raw, dict) else raw
        prefs = [r.get("memory", "") for r in items if r.get("memory")]
        logger.info("Memory fetch | user=%s | %d entries", user_id, len(prefs))
        return prefs
    except Exception as exc:
        logger.warning("Memory fetch failed: %s", exc)
        return []