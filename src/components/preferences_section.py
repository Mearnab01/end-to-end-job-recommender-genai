import streamlit as st
from src.memory.user_memory import get_preferences


def render_preferences(user_id: str) -> None:
    """
    Fetches the user's remembered searches from mem0 and
    displays them as a compact row of chips.
    Hidden entirely if no preferences exist or mem0 is not configured.
    """
    prefs = get_preferences(str(user_id))

    if not prefs:
        return

    chips_html = "".join(
        f'<span class="pref-chip">'
        f'<span class="material-icons-round" style="font-size:13px;vertical-align:middle;">history</span>'
        f'&nbsp;{p}</span>'
        for p in prefs[:6]
    )

    st.markdown(
        f"""
        <div class="pref-bar">
            <span class="pref-label">
                <span class="material-icons-round mi">auto_awesome</span>
                Recent searches
            </span>
            {chips_html}
        </div>
        """,
        unsafe_allow_html=True,
    )