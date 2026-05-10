import streamlit as st


# =========================================
# PRIVATE HTML HELPERS
# =========================================

def _source_badge(source: str) -> str:
    cls = "badge-linkedin" if source == "linkedin" else "badge-naukri"
    label = "LinkedIn" if source == "linkedin" else "Naukri"
    return f'<span class="source-badge {cls}">{label}</span>'


def _meta_item(icon: str, value: str) -> str:
    if not value:
        return ""
    return (
        f'<span class="job-meta-item">'
        f'<span class="material-icons-round mi">{icon}</span>'
        f'{value}</span>'
    )


def _skill_chips(skills: list) -> str:
    if not skills:
        return ""
    chips = "".join(
        f'<span class="skill-chip">{s}</span>'
        for s in skills[:8]
    )
    return f'<div class="skills-row">{chips}</div>'


# =========================================
# PUBLIC: render one job card
# =========================================

def render_job_card(job: dict) -> None:
    """
    Renders a single normalised job dict (JobListing.model_dump()).
    Works for both LinkedIn and Naukri jobs since they share one schema.
    """
    st.markdown('<hr class="job-divider">', unsafe_allow_html=True)

    col_logo, col_info = st.columns([1, 7], gap="medium")

    with col_logo:
        logo = job.get("logo", "")
        if logo:
            st.image(logo, width=60)
        else:
            st.markdown(
                """
                <div class="logo-placeholder">
                    <span class="material-icons-round" style="font-size:26px;">business</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_info:
        meta_html = (
            _meta_item("business",         job.get("company", ""))
            + _meta_item("location_on",    job.get("location", ""))
            + _meta_item("trending_up",    job.get("experience", ""))
            + _meta_item("payments",       job.get("salary", ""))
            + _meta_item("schedule",       job.get("posted_time", ""))
            + _meta_item("group",          job.get("applicants", ""))
            + _meta_item("work_outline",   job.get("work_type", ""))
        )

        skills_html = _skill_chips(job.get("skills", []))

        st.markdown(
            f"""
            <div class="job-card">
                <div class="job-title-row">
                    <span class="job-title">{job.get("title", "Untitled Role")}</span>
                    {_source_badge(job.get("source", ""))}
                </div>
                <div class="job-meta">{meta_html}</div>
                {skills_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Action buttons
        apply_url   = job.get("url", "")
        company_url = job.get("company_url", "")

        btn1, btn2, _ = st.columns([2, 2, 6])
        with btn1:
            if apply_url:
                st.link_button("Apply Now", apply_url, use_container_width=True)
        with btn2:
            if company_url:
                label = "Company Page" if job.get("source") == "linkedin" else "More Jobs"
                st.link_button(label, company_url, use_container_width=True)

        # Description expander
        description = job.get("description", "")
        if description:
            with st.expander("View Job Description"):
                st.write(description[:3000])