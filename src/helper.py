import fitz
import os
import time
import threading

import streamlit as st
from dotenv import load_dotenv
from google import genai
from groq import Groq

from utils.logger import get_logger

load_dotenv()

logger = get_logger("helper")

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GROQ_API_KEY   = st.secrets["GROQ_API_KEY"]

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client   = Groq(api_key=GROQ_API_KEY)

# =========================================
# SYSTEM PROMPT
# =========================================

SYS_PROMPT = """
You are CareerCopilot AI — an elite ATS resume analyzer and career assistant.

Rules you MUST follow on every response:
- Be concise. No filler, no preamble, no openers like "Great!" or "Sure!".
- Use bullet points for lists. Maximum 5 bullets per section.
- Bold section headers with **.
- Never repeat information across sections.
- Do not hallucinate skills, experience, or credentials.
- Each bullet must be one line — no nested sub-bullets.
- Total response must stay within the token limit given.
"""


# =========================================
# PROMPT TEMPLATES
# =========================================

SUMMARY_PROMPT = """
Analyze this resume. Return ONLY the structure below. No intro. No outro.
Format Rules:
- Convert all text wrapped inside ** ** into proper markdown bold
- Keep clean spacing and line breaks
- Use bullet points where needed
- Do NOT return raw ** symbols in output

**Role:** [target role / level inferred from resume]
**Skills:** [top 6 technical skills, comma-separated]
**Education:** [degree · institution · year/GPA]
**Experience:** [X years · key domains]
**Highlights:**
- [strongest achievement 1]
- [strongest achievement 2]
- [strongest achievement 3]

Resume:
{resume}
"""

GAPS_PROMPT = """
Identify gaps and improvements for this resume.
Return ONLY the structure below. No intro. No outro.

**ATS Score:** X / 10
**Missing Skills:**
- [skill 1]
- [skill 2]
- [skill 3]
**Weak Areas:**
- [weakness 1]
- [weakness 2]
**Quick Wins:**
- [actionable fix 1]
- [actionable fix 2]
- [actionable fix 3]

Resume:
{resume}
"""

ROADMAP_PROMPT = """
Write a focused 6-month career roadmap for this candidate.
Return ONLY the structure below. No intro. No outro. One line per bullet.

**Learn:**
- [skill/tool + why, one line]
- [skill/tool + why, one line]
- [skill/tool + why, one line]
**Certify:**
- [cert name + platform, one line]
- [cert name + platform, one line]
**Build:**
- [project idea, one line]
- [project idea, one line]
**Strategy:**
- [career move 1]
- [career move 2]
- [career move 3]

Resume:
{resume}
"""

KEYWORDS_PROMPT = """
Return ONLY a comma-separated list of job search keywords based on this resume summary.
No explanation. No numbering. Just the keywords.

Resume Summary:
{summary}
"""


# =========================================
# PDF EXTRACTION
# =========================================

def extract_text_from_pdf(upload_pdf) -> str:
    text = ""
    try:
        with fitz.open(stream=upload_pdf.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        logger.info("PDF extracted | chars=%d", len(text))
    except Exception as exc:
        logger.error("PDF extraction failed: %s", exc)
        st.error(f"PDF extraction failed: {exc}")
    return text


# =========================================
# LLM WRAPPERS
# =========================================

def ask_gemini(prompt: str) -> str:
    logger.debug("Gemini call | prompt_len=%d", len(prompt))
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        config={"system_instruction": SYS_PROMPT},
        contents=prompt,
    )
    logger.info("Gemini response | chars=%d", len(response.text))
    return response.text


def ask_groq(prompt: str, max_tokens: int = 400) -> str:
    logger.debug("Groq call | max_tokens=%d | prompt_len=%d", max_tokens, len(prompt))
    t0 = time.time()
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        temperature=0.4,
        max_tokens=max_tokens,
    )
    result = response.choices[0].message.content
    logger.info("Groq response | chars=%d | elapsed=%.2fs", len(result), time.time() - t0)
    return result


# =========================================
# PROGRESS BAR RUNNER
# =========================================

def run_with_progress(label: str, func, *args, **kwargs):
    """
    Runs func(*args, **kwargs) in a background thread while showing
    a smooth animated progress bar that crawls to 90% then snaps to 100%.
    """
    result   = [None]
    exc      = [None]
    finished = [False]

    def _worker():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exc[0] = e
        finally:
            finished[0] = True

    threading.Thread(target=_worker, daemon=True).start()

    bar = st.progress(0, text=label)
    pct = 0

    while not finished[0]:
        step = 4 if pct < 40 else (2 if pct < 70 else 1)
        pct  = min(pct + step, 90)
        bar.progress(pct, text=label)
        time.sleep(0.12)

    bar.progress(100, text="Done")
    time.sleep(0.25)
    bar.empty()

    if exc[0]:
        logger.error("run_with_progress '%s' failed: %s", label, exc[0])
        raise exc[0]

    return result[0]