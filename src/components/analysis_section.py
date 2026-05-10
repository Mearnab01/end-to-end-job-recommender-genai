import streamlit as st


def _card(icon: str, label: str, content: str) -> str:
    return f"""
    <div class="analysis-card">
        <div class="card-title">
            <span class="material-icons-round mi">{icon}</span>
            {label}
        </div>
        <div class="card-content">{content}</div>
    </div>
    """


def _success_banner(message: str):
    st.markdown(
        f"""
        <div class="success-banner">
            <span class="material-icons-round mi">check_circle</span>
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------
# Public render function
# ------------------------------------------------------------------

def render_analysis(summary: str, gaps: str, roadmap: str):
    _success_banner("Resume analysis completed successfully.")

    # ---- Row 1 : summary + skill gaps side by side ----
    st.markdown(
        """
        <div class="section-label">
            <span class="material-icons-round mi">analytics</span>
            AI Analysis
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        st.markdown(
            _card("summarize", "Resume Summary", summary),
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            _card("build", "Skill Gap Analysis", gaps),
            unsafe_allow_html=True,
        )

    # ---- Row 2 : roadmap full-width ----
    st.markdown(
        """
        <div class="section-label" style="margin-top:24px;">
            <span class="material-icons-round mi">map</span>
            Career Roadmap
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        _card("route", "Your Path Forward", roadmap),
        unsafe_allow_html=True,
    )