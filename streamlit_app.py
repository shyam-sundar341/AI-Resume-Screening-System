import streamlit as st
import pdfplumber
import tempfile

skills_db = [
    "python",
    "machine learning",
    "deep learning",
    "sql",
    "nlp",
    "flask",
    "django",
    "html",
    "css",
    "javascript",
    "tensorflow",
    "pytorch",
    "excel",
    "power bi"
]

JOB_DESCRIPTION = "Python Machine Learning"
REQUIRED_SKILLS = ["python", "machine learning"]


def extract_text_from_pdf(uploaded_file):
    text = ""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    with pdfplumber.open(temp_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    return text.lower()


def extract_skills(text):
    found = []

    for skill in skills_db:
        if skill.lower() in text.lower():
            found.append(skill)

    return list(set(found))


def calculate_match(candidate_skills, required_skills):
    matched = set(candidate_skills).intersection(set(required_skills))

    score = (len(matched) / len(required_skills)) * 100

    return round(score, 2)


def missing_skills(candidate_skills, required_skills):
    return list(set(required_skills) - set(candidate_skills))


def suggest_improvements(missing):
    return [f"Add projects related to {skill}" for skill in missing]


if "applications" not in st.session_state:
    st.session_state.applications = []

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "current_application" not in st.session_state:
    st.session_state.current_application = None


st.set_page_config(
    page_title="Technical Technologies",
    page_icon="🤖",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #07172e, #020409 70%);
        color: white;
    }

    .main-title {
        font-size: 64px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #1e90ff, #8a5cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        letter-spacing: 6px;
        color: #d8d8d8;
        font-size: 18px;
    }

    .card {
        padding: 25px;
        border-radius: 18px;
        background: rgba(10, 18, 35, 0.95);
        border: 1px solid #243b5c;
        box-shadow: 0 0 20px rgba(0, 123, 255, 0.12);
        margin-bottom: 25px;
    }

    .skill {
        display: inline-block;
        margin: 6px;
        padding: 10px 18px;
        border-radius: 10px;
        background: #091a33;
        border: 1px solid #1d5eff;
        color: white;
    }

    .score {
        font-size: 56px;
        font-weight: bold;
        color: #4aa3ff;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 class='main-title'>Technical technologies</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>AI RESUME SCREENING SYSTEM</p>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='card'>
        <h3>💼 Job Description</h3>
        <p>
        Looking for AI/ML candidates with strong Python and Machine Learning skills.
        The candidate should be able to build AI applications and develop ML models.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<div class='card'><h3>⭐ Required Skills</h3>",
    unsafe_allow_html=True
)

for skill in REQUIRED_SKILLS:
    st.markdown(
        f"<span class='skill'>{skill.title()}</span>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='card'><h3>👤 Candidate Details</h3>",
    unsafe_allow_html=True
)

name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

analyze = st.button("🚀 Analyze Resume")

st.markdown("</div>", unsafe_allow_html=True)

if analyze:

    if not name or not email or not phone or resume is None:
        st.error("Please fill all details and upload a PDF resume.")

    else:
        resume_text = extract_text_from_pdf(resume)

        candidate_skills = extract_skills(resume_text)

        score = calculate_match(
            candidate_skills,
            REQUIRED_SKILLS
        )

        missing = missing_skills(
            candidate_skills,
            REQUIRED_SKILLS
        )

        suggestions = suggest_improvements(missing)

        status = "Eligible" if score >= 70 else "Not Eligible"

        st.session_state.analysis_done = True

        st.session_state.current_application = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Score": score,
            "Status": status
        }

        st.session_state.current_result = {
            "name": name,
            "email": email,
            "phone": phone,
            "score": score,
            "status": status,
            "candidate_skills": candidate_skills,
            "missing": missing,
            "suggestions": suggestions
        }

if st.session_state.analysis_done and st.session_state.current_result:

    result = st.session_state.current_result

    st.markdown(
        "<div class='card'><h3>📊 Resume Analysis Report</h3>",
        unsafe_allow_html=True
    )

    st.write(f"**Name:** {result['name']}")
    st.write(f"**Email:** {result['email']}")
    st.write(f"**Phone:** {result['phone']}")

    st.markdown(
        f"<div class='score'>{result['score']}%</div>",
        unsafe_allow_html=True
    )

    st.progress(int(result["score"]))

    if result["status"] == "Eligible":
        st.success("✅ Eligible to Apply")
    else:
        st.error("❌ Not Eligible")

    st.subheader("✅ Skills Matched")

    if result["candidate_skills"]:
        for skill in result["candidate_skills"]:
            st.markdown(
                f"<span class='skill'>{skill.title()}</span>",
                unsafe_allow_html=True
            )
    else:
        st.warning("No matching skills found.")

    st.subheader("⚠️ Missing Skills")

    if result["missing"]:
        for skill in result["missing"]:
            st.error(skill.title())
    else:
        st.success("No missing skills found 🎉")

    st.subheader("💡 Suggestions")

    if result["suggestions"]:
        for suggestion in result["suggestions"]:
            st.write("- " + suggestion)
    else:
        st.success("Excellent resume match!")

    st.markdown("</div>", unsafe_allow_html=True)

    if result["status"] == "Eligible":

        if st.button("🚀 Apply Now"):

            st.session_state.applications.append(
                st.session_state.current_application
            )

            st.success("Application Submitted Successfully!")