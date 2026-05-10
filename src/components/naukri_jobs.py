import streamlit as st


# ------------------------------------------------------------------
# Private helpers
# ------------------------------------------------------------------

def _meta_item(icon: str, value: str) -> str:
    if not value or value == "N/A":
        return ""
    return f"""
    <span class="job-meta-item">
        <span class="material-icons-round mi">{icon}</span>
        {value}
    </span>
    """


def _render_skill_chips(skills_str: str) -> str:
    if not skills_str:
        return ""
    chips = "".join(
        f'<span class="skill-chip">{s.strip()}</span>'
        for s in skills_str.split(",")[:10]
    )
    return f'<div class="skills-row">{chips}</div>'


def _render_single_job(job: dict):
    title           = job.get("title", "Untitled Role")
    company         = job.get("companyName", "Unknown Company")
    location        = job.get("location", "")
    experience      = job.get("experience", "")
    salary          = job.get("salary", "Not Disclosed")
    footer_label    = job.get("footerPlaceholderLabel", "")
    skills_str      = job.get("tagsAndSkills", "")
    description     = job.get("jobDescription", "")
    logo            = job.get("logoPathV3", "")
    apply_url       = job.get("jdURL", "")
    more_jobs_url   = job.get("companyJobsUrl", "")

    st.markdown('<hr class="job-divider">', unsafe_allow_html=True)

    col_logo, col_info = st.columns([1, 7], gap="medium")

    with col_logo:
        if logo:
            st.image(logo, width=60)
        else:
            st.markdown(
                """
                <div class="logo-placeholder">
                    <span class="material-icons-round" style="font-size:28px;">business</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_info:
        meta_html = (
            _meta_item("business", company)
            + _meta_item("location_on", location)
            + _meta_item("trending_up", experience)
            + _meta_item("payments", salary)
            + _meta_item("schedule", footer_label)
        )

        skills_html = _render_skill_chips(skills_str)

        st.markdown(
            f"""
            <div class="job-card">
                <div class="job-title">{title}</div>
                <div class="job-meta">{meta_html}</div>
                {skills_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        btn_col1, btn_col2, _ = st.columns([2, 2, 6])

        with btn_col1:
            if apply_url:
                st.link_button(
                    "Apply Now",
                    apply_url,
                    use_container_width=True,
                )

        with btn_col2:
            if more_jobs_url:
                st.link_button(
                    "More Jobs",
                    more_jobs_url,
                    use_container_width=True,
                )

        if description:
            with st.expander("View Job Description"):
                st.write(description[:3000])


# ------------------------------------------------------------------
# Public render function
# ------------------------------------------------------------------

def render_naukri_jobs(jobs: list):
    st.markdown(
        """
        <div class="section-label">
            <span class="material-icons-round mi">apartment</span>
            Naukri Jobs
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not jobs:
        st.markdown(
            """
            <div class="warn-banner">
                <span class="material-icons-round mi">info</span>
                No Naukri jobs found for the current keywords.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for job in jobs[:10]:
        _render_single_job(job)