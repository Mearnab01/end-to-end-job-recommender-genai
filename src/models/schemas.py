from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# =========================================
# USER
# =========================================

class UserModel(BaseModel):
    id: int
    username: str
    created_at: Optional[str] = None
    is_new: bool = False


# =========================================
# JOB LISTING  (unified schema for both sources)
# =========================================

class JobListing(BaseModel):
    title:       str          = ""
    company:     str          = ""
    location:    str          = ""
    experience:  str          = ""
    salary:      str          = ""
    skills:      List[str]    = Field(default_factory=list)
    description: str          = ""
    url:         str          = ""
    source:      str          = ""   # "linkedin" | "naukri"
    logo:        str          = ""
    company_url: str          = ""
    posted_time: str          = ""
    applicants:  str          = ""
    work_type:   str          = ""


# =========================================
# RESUME ANALYSIS
# =========================================

class ResumeAnalysis(BaseModel):
    summary:  str
    gaps:     str
    roadmap:  str
    keywords: str = ""


# =========================================
# KEYWORD SEARCH  (validates search input)
# =========================================

class KeywordSearch(BaseModel):
    keywords: str = Field(..., min_length=2, max_length=300)

    @field_validator("keywords")
    @classmethod
    def strip_and_check(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Keywords must not be blank")
        return cleaned


# =========================================
# CACHED SEARCH  (stored/loaded from SQLite)
# =========================================

class CachedSearch(BaseModel):
    keywords:   str
    source:     str
    jobs:       List[JobListing]
    cached_at:  datetime
    expires_at: datetime


# =========================================
# NORMALIZERS  (raw scraper dict → JobListing)
# =========================================

def normalize_linkedin_job(raw: dict) -> JobListing:
    return JobListing(
        title       = raw.get("title", ""),
        company     = raw.get("companyName", ""),
        location    = raw.get("location", ""),
        experience  = raw.get("experienceLevel", ""),
        salary      = "",
        skills      = [],
        description = raw.get("description", ""),
        url         = raw.get("applyUrl") or raw.get("jobUrl") or "",
        source      = "linkedin",
        logo        = raw.get("companyLogo", ""),
        company_url = raw.get("companyUrl", ""),
        posted_time = raw.get("postedTime", ""),
        applicants  = str(raw.get("applicationsCount", "")),
        work_type   = raw.get("workType", ""),
    )


def normalize_naukri_job(raw: dict) -> JobListing:
    skills_raw = raw.get("tagsAndSkills", "")
    skills = [s.strip() for s in skills_raw.split(",") if s.strip()] if skills_raw else []

    return JobListing(
        title       = raw.get("title", ""),
        company     = raw.get("companyName", ""),
        location    = raw.get("location", ""),
        experience  = raw.get("experience", ""),
        salary      = raw.get("salary", ""),
        skills      = skills,
        description = raw.get("jobDescription", ""),
        url         = raw.get("jdURL", ""),
        source      = "naukri",
        logo        = raw.get("logoPathV3", ""),
        company_url = raw.get("companyJobsUrl", ""),
        posted_time = raw.get("footerPlaceholderLabel", ""),
        applicants  = "",
        work_type   = "",
    )