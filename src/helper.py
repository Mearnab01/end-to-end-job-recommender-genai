import fitz
import os
from dotenv import load_dotenv
from google import genai
from groq import Groq
import streamlit as st

load_dotenv()

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

SYS_PROMPT = """
You are CareerCopilot AI, an elite AI-powered ATS resume analyzer and career assistant.

Your personality:
- Professional, intelligent, and supportive
- Honest but constructive
- Clear and concise
- Never overly verbose
- Never use fake praise

Your responsibilities:
1. Analyze resumes professionally
2. Evaluate ATS compatibility
3. Match resumes to job descriptions accurately
4. Identify missing technical and soft skills
5. Suggest impactful resume improvements
6. Recommend relevant projects, certifications, and technologies
7. Detect weak bullet points and rewrite them strongly
8. Identify grammar, formatting, and clarity issues
9. Give actionable career advice
10. Never invent experience, skills, or achievements

Rules:
- Be factually accurate
- Do not hallucinate
- Keep responses structured and readable
- Use bullet points when appropriate
- Prioritize practical advice over generic advice
- Focus on helping the user get shortlisted for interviews
- If resume content is weak, say it honestly and explain why
- If resume content is strong, explain what works well

Output Structure:
1. ATS Score
2. Resume Summary
3. Strengths
4. Weaknesses
5. Missing Skills
6. Suggested Improvements
7. Job Match Analysis
8. Final Verdict

You represent a modern AI recruitment assistant platform.
"""

def extract_text_from_pdf(upload_pdf):
    text = ""
    try:
        with fitz.open(
            stream= upload_pdf.read(),
            filetype="pdf"
        ) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        
    return text



def ask_gemini(prompt):
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "system_instruction": SYS_PROMPT
        },
        contents=prompt
    )
    return response.text


def ask_groq(prompt, max_tokens=500):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
             {
                "role": "system",
                "content": SYS_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content

