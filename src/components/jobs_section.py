import streamlit as st
from src.components.job_card import render_job_card


# =========================================
# PRIVATE: cache status banner
# =========================================

def _cache_banner(from_cache: bool) -> None:
    if from_cache:
        st.markdown(
            """
            <div class="cache-hit-banner">
                <span class="material-icons-round mi">bolt</span>
                Results served from cache &mdash; no Apify call made.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="cache-miss-banner">
                <span class="material-icons-round mi">cloud_download</span>
                Fresh results fetched &mdash; saved to cache for next time.
            </div>
            """,
            unsafe_allow_html=True,
        )


def _empty_state(source: str) -> None:
    st.markdown(
        f"""
        <div class="warn-banner">
            <span class="material-icons-round mi">info</span>
            No {source} jobs found for these keywords.
        </div>
        """,
        unsafe_allow_html=True,
    )


def _section_label(icon: str, title: str) -> None:
    st.markdown(
        f"""
        <div class="section-label">
            <span class="material-icons-round mi">{icon}</span>
            {title}
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================
# PUBLIC: render full jobs section
# =========================================

def render_jobs(
    linkedin_jobs: list,
    naukri_jobs:   list,
    from_cache:    bool,
) -> None:
    """
    Renders the cache status indicator then both job lists
    using the unified job_card component.
    """

    _cache_banner(from_cache)

    # ---- LinkedIn ----
    _section_label("work", "LinkedIn Jobs")

    if linkedin_jobs:
        for job in linkedin_jobs[:10]:
            render_job_card(job)
    else:
        _empty_state("LinkedIn")

    # ---- Naukri ----
    _section_label("apartment", "Naukri Jobs")

    if naukri_jobs:
        for job in naukri_jobs[:10]:
            render_job_card(job)
    else:
        _empty_state("Naukri")