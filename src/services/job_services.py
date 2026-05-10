"""
Job service: single entry point for fetching jobs.

Flow:
  1. Check SQLite cache for both sources.
  2. If both cached → return immediately (no Apify call).
  3. If either/both missing → call Apify, normalise, save to cache.

Returns: (linkedin_jobs, naukri_jobs, from_cache)
  where each jobs list contains normalised dicts (JobListing.model_dump()).
"""

from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs
from src.cache.job_cache import get_cached_jobs, save_jobs_to_cache
from src.models.schemas import normalize_linkedin_job, normalize_naukri_job
from utils.logger import get_logger

logger = get_logger("job_service")


def get_jobs(keywords: str, rows: int = 15) -> tuple[list, list, bool]:
    """
    Returns (linkedin_jobs, naukri_jobs, from_cache).
    All job items are plain dicts following the unified JobListing schema.
    """

    # ----------------------------------------
    # 1. Try cache first
    # ----------------------------------------
    linkedin_cached = get_cached_jobs(keywords, "linkedin")
    naukri_cached   = get_cached_jobs(keywords, "naukri")

    if linkedin_cached is not None and naukri_cached is not None:
        logger.info("Serving jobs from cache | keywords=%.40s", keywords)
        return linkedin_cached, naukri_cached, True

    # ----------------------------------------
    # 2. Fetch fresh from Apify
    # ----------------------------------------
    logger.info("Fetching fresh jobs from Apify | keywords=%.40s", keywords)

    raw_linkedin = fetch_linkedin_jobs(keywords, rows=rows) or []
    raw_naukri   = fetch_naukri_jobs(keywords, rows=rows)   or []

    logger.info(
        "Apify response | linkedin=%d | naukri=%d",
        len(raw_linkedin), len(raw_naukri),
    )

    # ----------------------------------------
    # 3. Normalise to unified schema
    # ----------------------------------------
    linkedin_jobs = [normalize_linkedin_job(j).model_dump() for j in raw_linkedin]
    naukri_jobs   = [normalize_naukri_job(j).model_dump()   for j in raw_naukri]

    # ----------------------------------------
    # 4. Save to cache
    # ----------------------------------------
    if linkedin_jobs:
        save_jobs_to_cache(keywords, "linkedin", linkedin_jobs)
    if naukri_jobs:
        save_jobs_to_cache(keywords, "naukri",   naukri_jobs)

    return linkedin_jobs, naukri_jobs, False