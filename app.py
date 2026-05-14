import streamlit as st
import pdfplumber
import pandas as pd
from io import StringIO

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

    /* Main Background */
    .stApp {
        background: linear-gradient(to right, #f8fbff, #eef4ff);
    }

    /* Header Style */
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #475569;
        margin-bottom: 35px;
    }

    /* Card Design */
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* Score Box */
    .score-box {
        background: linear-gradient(to right, #2563EB, #1D4ED8);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-size: 32px;
        font-weight: bold;
    }

    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 8px 14px;
        border-radius: 12px;
        margin: 5px;
        font-size: 14px;
        font-weight: 500;
    }

    .missing-tag {
        display: inline-block;
        background-color: #FEE2E2;
        color: #B91C1C;
        padding: 8px 14px;
        border-radius: 12px;
        margin: 5px;
        font-size: 14px;
        font-weight: 500;
    }

</style>
""", unsafe_allow_html=True)

# ---------------- SKILLS ---------------- #
skills = [
    "python",
    "sql",
    "machine learning",
    "pandas",
    "numpy",
    "power bi",
    "data visualization",
    "deep learning",
    "natural language processing",
    "data analysis",
    "github",
    "cloud computing",
    "excel",
    "tableau",
    "streamlit",
    "tensorflow",
    "communication",
    "problem solving"
]

# ---------------- PDF TEXT EXTRACTION ---------------- #
def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text.lower()

# ---------------- HEADER ---------------- #
st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle"> Give me a Sign, If the Job is Mine `</div>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("✨ Features")

st.sidebar.info("""
✅ Resume Score Analysis

✅ Skills Detection

✅ Missing Skills Suggestion

✅ LinkedIn & GitHub Check

✅ Beginner Friendly AI Project

""")

# ---------------- FILE UPLOAD ---------------- #
uploaded_file = st.file_uploader(
    "📤 Upload Your Resume",
    type=["pdf"]
)

# ---------------- MAIN LOGIC ---------------- #
if uploaded_file:

    with st.spinner("Analyzing Resume..."):

        resume_text = extract_text(uploaded_file)

        found_skills = []
        missing_skills = []

        # Skill Matching
        for skill in skills:

            if skill in resume_text:
                found_skills.append(skill)

            else:
                missing_skills.append(skill)

        # Score Calculation
        score = int((len(found_skills) / len(skills)) * 100)

    # ---------------- SCORE SECTION ---------------- #
    st.markdown(
        f"""
        <div class="score-box">
            Resume Score <br>
            {score}/100
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # ---------------- COLUMNS ---------------- #
    col1, col2 = st.columns(2)

    # FOUND SKILLS
    with col1:

        st.markdown(
            '<div class="card"><h3>✅ Skills Found</h3>',
            unsafe_allow_html=True
        )

        if found_skills:

            for skill in found_skills:

                st.markdown(
                    f'<span class="skill-tag">{skill.title()}</span>',
                    unsafe_allow_html=True
                )

        else:
            st.write("No matching skills found.")

        st.markdown('</div>', unsafe_allow_html=True)

    # MISSING SKILLS
    with col2:

        st.markdown(
            '<div class="card"><h3>❌ Missing Skills</h3>',
            unsafe_allow_html=True
        )

        if missing_skills:

            for skill in missing_skills:

                st.markdown(
                    f'<span class="missing-tag">{skill.title()}</span>',
                    unsafe_allow_html=True
                )

        else:
            st.write("Great! No missing skills.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- SUGGESTIONS ---------------- #
    st.markdown(
        '<div class="card"><h3>💡 Suggestions</h3>',
        unsafe_allow_html=True
    )

    if "github" not in resume_text:
        st.warning("Add your GitHub profile to improve technical credibility.")

    if "linkedin" not in resume_text:
        st.warning("Add your LinkedIn profile for professional visibility.")

    if score < 50:
        st.error("Your resume needs improvement. Add more technical skills and projects.")

    elif score < 75:
        st.info("Good resume! Add a few more industry-level skills to improve.")

    else:
        st.success("Excellent resume! You are job ready 🚀")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- DATA TABLE ---------------- #
    st.markdown(
        '<div class="card"><h3>📊 Skill Report</h3>',
        unsafe_allow_html=True
    )

    report_data = {
        "Found Skills": found_skills,
        "Missing Skills": missing_skills[:len(found_skills)]
    }

    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in report_data.items()]))

    st.dataframe(df, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
