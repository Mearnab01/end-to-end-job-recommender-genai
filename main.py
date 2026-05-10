import streamlit as st

from src.helper import (
    extract_text_from_pdf,
    ask_groq
)

from src.job_api import (
    fetch_linkedin_jobs,
    fetch_naukri_jobs
)

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Job Recommender",
    page_icon="🚀",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #1f2937;
    margin-bottom: 20px;
}

.job-card {
    background-color: #0f172a;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1e293b;
    margin-bottom: 14px;
}

.small-text {
    color: #9ca3af;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================

st.title("🚀 AI Resume Job Recommender")

st.caption(
    "Upload your resume and get AI-powered insights, "
    "skill gap analysis, roadmap suggestions, "
    "and job recommendations."
)

# =========================================
# FILE UPLOAD
# =========================================

uploaded_file = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf"]
)

# =========================================
# MAIN APP
# =========================================

if uploaded_file:

    # -------------------------------
    # Extract Resume
    # -------------------------------

    with st.spinner("📄 Extracting resume text..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    # -------------------------------
    # AI Analysis
    # -------------------------------

    with st.spinner("🧠 Running AI analysis..."):

        summary = ask_groq(f"""
        Analyze this resume professionally.

        Return:
        - Short summary
        - Skills
        - Education
        - Experience

        Resume:
        {resume_text}
        """)

        gaps = ask_groq(f"""
        Analyze missing skills, certifications,
        weak areas, and improvement opportunities.

        Resume:
        {resume_text}
        """)

        roadmap = ask_groq(f"""
        Create a future roadmap for this candidate.

        Include:
        - Skills to learn
        - Certifications
        - Projects
        - Career strategy

        Resume:
        {resume_text}
        """)

    # =========================================
    # RESULTS SECTION
    # =========================================

    st.success("✅ Resume Analysis Completed")

    col1, col2 = st.columns(2)

    # -------------------------------
    # SUMMARY
    # -------------------------------

    with col1:

        st.markdown("## 📑 Resume Summary")

        st.markdown(
            f"""
            <div class="card">
            {summary}
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------
    # SKILL GAPS
    # -------------------------------

    with col2:

        st.markdown("## 🛠️ Skill Gap Analysis")

        st.markdown(
            f"""
            <div class="card">
            {gaps}
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------
    # ROADMAP
    # -------------------------------

    st.markdown("## 🚀 Career Roadmap")

    st.markdown(
        f"""
        <div class="card">
        {roadmap}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================================
    # JOB SECTION
    # =========================================

    if st.button("💼 Get Job Recommendations"):

        with st.spinner("🔎 Extracting job keywords..."):

            keywords = ask_groq(f"""
            Based on this resume,
            generate the BEST job search keywords.

            Return ONLY comma-separated keywords.

            Resume Summary:
            {summary}
            """)

            search_keywords = keywords.replace("\n", "").strip()

        st.info(f"🎯 Keywords: {search_keywords}")

        # =========================================
        # FETCH JOBS
        # =========================================

        with st.spinner("🌍 Fetching jobs..."):

            linkedin_jobs = fetch_linkedin_jobs(
                search_keywords,
                rows=15
            )

            naukri_jobs = fetch_naukri_jobs(
                search_keywords,
                rows=15
            )

        # =========================================
# LINKEDIN JOBS
# =========================================

st.markdown("## 🔵 LinkedIn Jobs")

if linkedin_jobs:

    for job in linkedin_jobs[:10]:

        job_link = (
            job.get("applyUrl")
            or job.get("jobUrl")
        )

        company_logo = job.get("companyLogo", "")

        with st.container():

            st.markdown("""
            <hr style='margin-top:10px;margin-bottom:10px;'>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 5])

            # =================================
            # COMPANY LOGO
            # =================================

            with col1:

                if company_logo:
                    st.image(company_logo, width=70)

            # =================================
            # JOB DETAILS
            # =================================

            with col2:

                st.subheader(f"💼 {job.get('title')}")

                st.markdown(
                    f"""
                    🏢 **{job.get('companyName', 'Unknown Company')}**  
                    📍 {job.get('location', 'N/A')}  
                    🧑‍💻 {job.get('experienceLevel', 'N/A')}  
                    🕒 {job.get('postedTime', 'N/A')}  
                    👥 {job.get('applicationsCount', 'N/A')}  
                    🏷️ {job.get('workType', 'N/A')}
                    """
                )

                # =============================
                # BUTTONS
                # =============================

                btn1, btn2 = st.columns(2)

                with btn1:
                    st.link_button(
                        "🔗 Apply Now",
                        job_link,
                        use_container_width=True
                    )

                with btn2:

                    company_url = job.get("companyUrl")

                    if company_url:
                        st.link_button(
                            "🏢 Company Page",
                            company_url,
                            use_container_width=True
                        )

                # =============================
                # SKILLS
                # =============================

                description = job.get("description", "")

                with st.expander("📄 View Job Description"):

                    st.write(description[:3000])

# =========================================
# NO JOBS
# =========================================

else:
    st.warning("No LinkedIn jobs found.")

# =========================================
# NAUKRI JOBS
# =========================================

st.markdown("## 🇮🇳 Naukri Jobs")

if naukri_jobs:

    for job in naukri_jobs[:10]:

        job_link = job.get("jdURL")

        company_logo = job.get("logoPathV3", "")

        with st.container():

            st.markdown("""
            <hr style='margin-top:10px;margin-bottom:10px;'>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 5])

            # =================================
            # COMPANY LOGO
            # =================================

            with col1:

                if company_logo:
                    st.image(company_logo, width=70)

            # =================================
            # JOB DETAILS
            # =================================

            with col2:

                st.subheader(f"💼 {job.get('title')}")

                st.markdown(
                    f"""
                    🏢 **{job.get('companyName', 'Unknown Company')}**  
                    📍 {job.get('location', 'N/A')}  
                    🧑‍💻 {job.get('experience', 'N/A')}  
                    💰 {job.get('salary', 'Not Disclosed')}  
                    🕒 {job.get('footerPlaceholderLabel', 'N/A')}
                    """
                )

                # =============================
                # SKILLS
                # =============================

                skills = job.get("tagsAndSkills")

                if skills:

                    skill_list = skills.split(",")

                    formatted_skills = " ".join(
                        [f"`{skill.strip()}`" for skill in skill_list[:10]]
                    )

                    st.markdown(
                        f"🛠️ Skills: {formatted_skills}"
                    )

                # =============================
                # BUTTONS
                # =============================

                btn1, btn2 = st.columns(2)

                with btn1:

                    st.link_button(
                        "🔗 Apply Now",
                        job_link,
                        use_container_width=True
                    )

                with btn2:

                    company_jobs_url = job.get("companyJobsUrl")

                    if company_jobs_url:

                        st.link_button(
                            "🏢 More Jobs",
                            company_jobs_url,
                            use_container_width=True
                        )

                # =============================
                # DESCRIPTION
                # =============================

                with st.expander("📄 View Job Description"):

                    st.write(
                        job.get("jobDescription", "")[:3000]
                    )

# =========================================
# NO JOBS
# =========================================

else:
    st.warning("No Naukri jobs found.")

        