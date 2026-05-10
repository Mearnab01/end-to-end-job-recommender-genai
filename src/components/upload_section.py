import streamlit as st


def render_upload() -> object:
    st.markdown(
        """
        <div class="section-label">
            <span class="material-icons-round mi">upload_file</span>
            Resume Upload
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"],
        label_visibility="collapsed",
    )

    return uploaded_file