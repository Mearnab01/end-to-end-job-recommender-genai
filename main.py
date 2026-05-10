import streamlit as st

from src.database.db import init_db
from src.styles import load_styles
from src.helper import (
    extract_text_from_pdf,
    ask_groq,
    run_with_progress,
    SUMMARY_PROMPT,
    GAPS_PROMPT,
    ROADMAP_PROMPT,
    KEYWORDS_PROMPT,
)
from src.models.schemas import KeywordSearch
from src.services.job_services import get_jobs
from src.memory.user_memory import save_search

from src.components.header import render_header
from src.components.auth_section import render_auth, render_greeting
from src.components.preferences_section import render_preferences
from src.components.upload_section import render_upload
from src.components.analysis_section import render_analysis
from src.components.jobs_section import render_jobs

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Career Pilot | AI Career Copilot",
    page_icon=":material/rocket_launch:",
    layout="wide",
)

# =========================================
# ONE-TIME STARTUP
# =========================================

init_db()   # creates SQLite tables if not present
load_styles()
render_header()

# =========================================
# AUTH GATE
# =========================================

user = render_auth()

if not user:
    st.stop()   # nothing below renders until user is logged in

# =========================================
# LOGGED-IN AREA
# =========================================

render_greeting(user)
render_preferences(user["id"])   # shows mem0 past searches (silent if none)

# =========================================
# FILE UPLOAD
# =========================================

uploaded_file = render_upload()

if not uploaded_file:
    st.stop()

# =========================================
# STEP 1 — Extract resume text
# =========================================

resume_text = run_with_progress(
    "Extracting resume text…",
    extract_text_from_pdf,
    uploaded_file,
)

if not resume_text or not resume_text.strip():
    st.error("Could not extract text from the PDF. Please try another file.")
    st.stop()

# =========================================
# STEP 2 — AI analysis (3 separate bars
#           so the user sees live progress)
# =========================================

summary = run_with_progress(
    "Analysing resume…",
    ask_groq,
    SUMMARY_PROMPT.format(resume=resume_text),
    400,
)

gaps = run_with_progress(
    "Identifying skill gaps…",
    ask_groq,
    GAPS_PROMPT.format(resume=resume_text),
    350,
)

roadmap = run_with_progress(
    "Building career roadmap…",
    ask_groq,
    ROADMAP_PROMPT.format(resume=resume_text),
    400,
)

# =========================================
# STEP 3 — Show analysis cards
# =========================================

render_analysis(summary, gaps, roadmap)

# =========================================
# STEP 4 — Job recommendations (on demand)
# =========================================

st.markdown(
    """
    <div class="section-label" style="margin-top:32px;">
        <span class="material-icons-round mi">work_history</span>
        Job Recommendations
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("Get Job Recommendations", type="primary"):

    # -- Extract & validate keywords --
    raw_keywords = run_with_progress(
        "Extracting job keywords…",
        ask_groq,
        KEYWORDS_PROMPT.format(summary=summary),
        120,
    )

    try:
        validated   = KeywordSearch(keywords=raw_keywords)
        search_kw   = validated.keywords
    except Exception:
        search_kw   = raw_keywords.replace("\n", "").strip()

    st.markdown(
        f"""
        <div class="keyword-banner">
            <span class="material-icons-round mi">travel_explore</span>
            &nbsp;<strong>Keywords:</strong>&nbsp;{search_kw}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -- Fetch jobs (cache-first, single progress bar) --
    jobs_result = run_with_progress(
        "Fetching jobs from LinkedIn & Naukri… Please wait for 1-2 mins…",
        get_jobs,
        search_kw,
        rows=15,
    )
    linkedin_jobs, naukri_jobs, from_cache = jobs_result

    # -- Save this search to mem0 (fire-and-forget, non-blocking) --
    save_search(str(user["id"]), search_kw)

    # -- Render jobs with cache badge --
    render_jobs(linkedin_jobs, naukri_jobs, from_cache)