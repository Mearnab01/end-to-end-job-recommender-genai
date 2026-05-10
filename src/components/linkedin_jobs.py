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


def _render_single_job(job: dict):
    title       = job.get("title", "Untitled Role")
    company     = job.get("companyName", "Unknown Company")
    location    = job.get("location", "")
    exp_level   = job.get("experienceLevel", "")
    posted      = job.get("postedTime", "")
    applicants  = job.get("applicationsCount", "")
    work_type   = job.get("workType", "")
    description = job.get("description", "")
    logo        = job.get("companyLogo", "")
    apply_url   = job.get("applyUrl") or job.get("jobUrl") or ""
    company_url = job.get("companyUrl", "")

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
            + _meta_item("signal_cellular_alt", exp_level)
            + _meta_item("schedule", posted)
            + _meta_item("group", applicants)
            + _meta_item("work_outline", work_type)
        )

        st.markdown(
            f"""
            <div class="job-card">
                <div class="job-title">{title}</div>
                <div class="job-meta">{meta_html}</div>
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
            if company_url:
                st.link_button(
                    "Company Page",
                    company_url,
                    use_container_width=True,
                )

        if description:
            with st.expander("View Job Description"):
                st.write(description[:3000])


# ------------------------------------------------------------------
# Public render function
# ------------------------------------------------------------------

def render_linkedin_jobs(jobs: list):
    st.markdown(
        """
        <div class="section-label">
            <span class="material-icons-round mi">work</span>
            LinkedIn Jobs
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not jobs:
        st.markdown(
            """
            <div class="warn-banner">
                <span class="material-icons-round mi">info</span>
                No LinkedIn jobs found for the current keywords.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for job in jobs[:10]:
        _render_single_job(job)