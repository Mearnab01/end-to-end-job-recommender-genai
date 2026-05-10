import streamlit as st
from src.auth.auth import login_or_register


def render_auth() -> dict | None:
    """
    Shows a login card if the user is not in session.
    Returns the user dict once authenticated, None otherwise.
    """
    if st.session_state.get("user"):
        return st.session_state["user"]

    # ---- Login card ----
    st.markdown(
        """
        <div class="auth-card">
            <div class="auth-title">
                <span class="material-icons-round mi">person_outline</span>
                Sign In
            </div>
            <p class="auth-subtitle">
                Enter any username to continue.
                New accounts are created automatically.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, col2, _ = st.columns([1, 8, 1])
    with col2:
        username = st.text_input(
            "Username",
            placeholder="e.g. arnab_nath",
            label_visibility="collapsed",
        )
        if st.button("Continue →", use_container_width=True, type="primary"):
            name = username.strip()
            if len(name) < 2:
                st.error("Username must be at least 2 characters.")
            else:
                user = login_or_register(name)
                st.session_state["user"] = user
                st.rerun()

    return None


def render_greeting(user: dict) -> None:
    """Shows a greeting bar with the username and a sign-out button."""
    msg = "Welcome aboard" if user.get("is_new") else "Welcome back"

    col_greet, col_out = st.columns([6, 1])

    with col_greet:
        st.markdown(
            f"""
            <div class="greeting-bar">
                <span class="material-icons-round" style="font-size:20px;vertical-align:middle;color:#4ade80;">
                    waving_hand
                </span>
                &nbsp;{msg}, <strong>{user['username']}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_out:
        if st.button("Sign out", use_container_width=True):
            del st.session_state["user"]
            st.rerun()