import json
import hashlib
from datetime import datetime, timedelta

from src.database.db import get_db_connection
from utils.logger import get_logger

logger = get_logger("cache")

CACHE_HOURS = 12  # cached jobs are valid for 12 hours


# =========================================
# INTERNAL HELPERS
# =========================================

def _hash_keywords(keywords: str) -> str:
    """
    Normalise keywords before hashing so that
    'Python, Django' and 'django, python' map to the same cache entry.
    """
    normalised = ",".join(sorted(
        k.strip().lower() for k in keywords.split(",") if k.strip()
    ))
    return hashlib.md5(normalised.encode()).hexdigest()


# =========================================
# PUBLIC API
# =========================================

def get_cached_jobs(keywords: str, source: str) -> list | None:
    """
    Returns a list of normalised job dicts if a fresh cache entry exists,
    or None on a cache miss / expired entry.
    """
    key_hash = _hash_keywords(keywords)
    now      = datetime.utcnow().isoformat()

    conn = get_db_connection()
    cur  = conn.cursor()

    cur.execute(
        """
        SELECT jobs_json FROM job_cache
        WHERE keyword_hash = ? AND source = ? AND expires_at > ?
        ORDER BY cached_at DESC
        LIMIT 1
        """,
        (key_hash, source, now),
    )
    row = cur.fetchone()
    conn.close()

    if row:
        logger.info("Cache HIT  | source=%-8s | keywords=%.40s", source, keywords)
        return json.loads(row["jobs_json"])

    logger.info("Cache MISS | source=%-8s | keywords=%.40s", source, keywords)
    return None


def save_jobs_to_cache(keywords: str, source: str, jobs: list) -> None:
    """Upserts a cache entry for this keyword+source combination."""
    if not jobs:
        return

    key_hash  = _hash_keywords(keywords)
    now       = datetime.utcnow()
    expires   = now + timedelta(hours=CACHE_HOURS)

    conn = get_db_connection()
    cur  = conn.cursor()

    # Remove any stale entries for this key first
    cur.execute(
        "DELETE FROM job_cache WHERE keyword_hash = ? AND source = ?",
        (key_hash, source),
    )

    cur.execute(
        """
        INSERT INTO job_cache
            (keyword_hash, keywords, source, jobs_json, cached_at, expires_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            key_hash,
            keywords,
            source,
            json.dumps(jobs),
            now.isoformat(),
            expires.isoformat(),
        ),
    )

    conn.commit()
    conn.close()

    logger.info(
        "Cache SAVE | source=%-8s | %d jobs | expires %s",
        source, len(jobs), expires.strftime("%H:%M UTC"),
    )