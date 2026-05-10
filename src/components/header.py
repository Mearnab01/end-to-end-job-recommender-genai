import streamlit as st


def render_header():
    st.markdown(
        """
        <div class="page-header">
            <h1>
                <span class="header-icon material-icons-round">rocket_launch</span>
                Career Pilot
            </h1>
            <p>
                Upload your resume and get AI-powered insights,
                skill gap analysis, career roadmap suggestions,
                and personalised job recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )