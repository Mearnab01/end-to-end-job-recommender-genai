import streamlit as st


def load_styles():
    st.markdown(
        """
        <style>
        
        @import url('https://fonts.googleapis.com/icon?family=Material+Icons+Round');
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap');


        html, body {
            font-family: 'DM Sans', sans-serif;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }

        /* ---- Icon helpers ---- */
        .mi {
            font-family: 'Material Icons Round';
            font-size: 18px;
            vertical-align: middle;
            line-height: 1;
            color: #60a5fa;
        }

        /* ---- Page header ---- */
        .page-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border: 1px solid #334155;
            border-radius: 20px;
            padding: 36px 40px;
            margin-bottom: 24px;
        }

        .page-header h1 {
            font-size: 2rem;
            font-weight: 600;
            color: #f1f5f9;
            margin: 0 0 8px 0;
            letter-spacing: -0.02em;
        }

        .page-header p {
            color: #94a3b8;
            font-size: 0.95rem;
            margin: 0;
            line-height: 1.6;
        }

        .header-icon {
            font-family: 'Material Icons Round';
            font-size: 36px;
            color: #3b82f6;
            vertical-align: middle;
            margin-right: 12px;
        }

        /* ---- Auth card ---- */
        .auth-card {
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 16px;
            padding: 28px 32px 16px 32px;
            margin-bottom: 16px;
            max-width: 100%;
        }

        .auth-title {
            font-size: 1rem;
            font-weight: 600;
            color: #f1f5f9;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .auth-subtitle {
            color: #64748b;
            font-size: 0.85rem;
            margin: 0;
            line-height: 1.6;
        }

        /* ---- Greeting bar ---- */
        .greeting-bar {
            background: #052e16;
            border: 1px solid #166534;
            border-radius: 10px;
            padding: 10px 18px;
            color: #86efac;
            font-size: 0.9rem;
            margin-bottom: 16px;
        }

        /* ---- Preferences bar ---- */
        .pref-bar {
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 10px 16px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }

        .pref-label {
            font-size: 0.78rem;
            font-weight: 600;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            display: flex;
            align-items: center;
            gap: 5px;
            margin-right: 4px;
        }

        .pref-chip {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: #1e293b;
            border: 1px solid #334155;
            color: #94a3b8;
            font-size: 0.78rem;
            padding: 3px 10px;
            border-radius: 20px;
        }

        /* ---- Section label ---- */
        .section-label {
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #475569;
            margin: 28px 0 14px 0;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 10px;
        }

        /* ---- Analysis cards ---- */
        .analysis-card {
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 16px;
            padding: 24px;
            height: 100%;
        }

        .card-title {
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #475569;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .card-title .mi {
            color: #3b82f6;
            font-size: 16px;
        }

        .card-content {
            color: #cbd5e1;
            font-size: 0.9rem;
            line-height: 1.8;
        }

        /* ---- Job card ---- */
        .job-card {
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 14px;
            padding: 18px 22px;
            margin-bottom: 4px;
        }

        .job-title-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }

        .job-title {
            font-size: 1rem;
            font-weight: 600;
            color: #f1f5f9;
        }

        .job-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 10px;
        }

        .job-meta-item {
            display: flex;
            align-items: center;
            gap: 4px;
            color: #94a3b8;
            font-size: 0.83rem;
        }

        .job-meta-item .mi {
            font-size: 14px;
            color: #475569;
        }

        /* ---- Source badges ---- */
        .source-badge {
            font-size: 0.7rem;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .badge-linkedin {
            background: #1d4ed820;
            border: 1px solid #1d4ed8;
            color: #93c5fd;
        }

        .badge-naukri {
            background: #92400e20;
            border: 1px solid #92400e;
            color: #fcd34d;
        }

        /* ---- Skill chips ---- */
        .skill-chip {
            display: inline-block;
            background: #1e293b;
            border: 1px solid #334155;
            color: #93c5fd;
            font-size: 0.73rem;
            font-family: 'DM Mono', monospace;
            padding: 2px 9px;
            border-radius: 5px;
            margin: 2px 3px 2px 0;
        }

        .skills-row {
            margin-bottom: 10px;
        }

        /* ---- Cache status banners ---- */
        .cache-hit-banner {
            background: #052e16;
            border: 1px solid #166534;
            border-radius: 10px;
            padding: 10px 18px;
            color: #86efac;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            margin-bottom: 16px;
        }

        .cache-miss-banner {
            background: #0c1a2e;
            border: 1px solid #1d4ed8;
            border-radius: 10px;
            padding: 10px 18px;
            color: #93c5fd;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            margin-bottom: 16px;
        }

        /* ---- Keyword banner ---- */
        .keyword-banner {
            background: #0f172a;
            border: 1px solid #1d4ed8;
            border-radius: 12px;
            padding: 12px 18px;
            color: #93c5fd;
            font-size: 0.85rem;
            margin-bottom: 20px;
            font-family: 'DM Mono', monospace;
        }

        /* ---- Success / warning banners ---- */
        .success-banner {
            background: #052e16;
            border: 1px solid #166534;
            border-radius: 12px;
            padding: 12px 18px;
            color: #86efac;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }

        .warn-banner {
            background: #1c1000;
            border: 1px solid #854d0e;
            border-radius: 12px;
            padding: 12px 18px;
            color: #fbbf24;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
        }

        /* ---- Logo placeholder ---- */
        .logo-placeholder {
            width: 56px;
            height: 56px;
            background: #1e293b;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #475569;
        }

        /* ---- Divider ---- */
        .job-divider {
            border: none;
            border-top: 1px solid #1e293b;
            margin: 4px 0 16px 0;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )