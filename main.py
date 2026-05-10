import streamlit as st

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
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

from src.components.header import render_header
from src.components.upload_section import render_upload
from src.components.analysis_section import render_analysis
from src.components.linkedin_jobs import render_linkedin_jobs
from src.components.naukri_jobs import render_naukri_jobs

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Job Recommender",
    page_icon="rocket_launch",
    layout="wide",
)

# =========================================
# STYLES + HEADER
# =========================================

load_styles()
render_header()

# =========================================
# FILE UPLOAD
# =========================================

uploaded_file = render_upload()

# =========================================
# MAIN FLOW
# =========================================

if uploaded_file:

    # ----------------------------------------
    # Step 1 – Extract resume text
    # ----------------------------------------

    resume_text = run_with_progress(
        "Extracting resume text…",
        extract_text_from_pdf,
        uploaded_file,
    )

    if not resume_text or not resume_text.strip():
        st.error("Could not extract text from the PDF. Please try another file.")
        st.stop()

    # ----------------------------------------
    # Step 2 – AI analysis, each with its own
    #           progress bar so users see motion
    # ----------------------------------------

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

    # ----------------------------------------
    # Step 3 – Render analysis cards
    # ----------------------------------------

    render_analysis(summary, gaps, roadmap)

    # ----------------------------------------
    # Step 4 – Job recommendations (on demand)
    # ----------------------------------------

    st.markdown(
        """
        <div class="section-label" style="margin-top:32px;">
            <span class="material-icons-round mi">work_history</span>
            Job Recommendations
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Get Job Recommendations", use_container_width=False):

        # -- Extract keywords --
        raw_keywords = run_with_progress(
            "Extracting job keywords…",
            ask_groq,
            KEYWORDS_PROMPT.format(summary=summary),
            120,
        )
        search_keywords = raw_keywords.replace("\n", "").strip()

        st.markdown(
            f"""
            <div class="keyword-banner">
                <span class="material-icons-round mi">travel_explore</span>
                &nbsp;<strong>Keywords:</strong>&nbsp;{search_keywords}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -- Fetch LinkedIn & Naukri with separate progress bars --
        linkedin_jobs = run_with_progress(
            "Fetching LinkedIn jobs…",
            fetch_linkedin_jobs,
            search_keywords,
            rows = 15,
        )

        naukri_jobs = run_with_progress(
            "Fetching Naukri jobs…",
            fetch_naukri_jobs,
            search_keywords,
            rows = 15,
        )

        # -- Render jobs --
        render_linkedin_jobs(linkedin_jobs)
        render_naukri_jobs(naukri_jobs)