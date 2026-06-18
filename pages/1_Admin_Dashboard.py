import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #07172e, #020409 70%);
        color: white;
    }

    .title {
        font-size: 54px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #1e90ff, #8a5cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        letter-spacing: 5px;
        color: #d8d8d8;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Login
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:

    st.markdown("<h1 class='title'>Technical technologies</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>RECRUITER LOGIN</p>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":
            st.session_state.admin_logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.stop()

# Dashboard
st.markdown("<h1 class='title'>Technical technologies</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>RECRUITER ANALYTICS DASHBOARD</p>", unsafe_allow_html=True)

if st.button("Logout"):
    st.session_state.admin_logged_in = False
    st.rerun()

if "applications" not in st.session_state:
    st.session_state.applications = []

applications = st.session_state.applications

total = len(applications)
eligible = len([a for a in applications if a["Status"] == "Eligible"])
rejected = total - eligible

col1, col2, col3 = st.columns(3)

col1.metric("Total Candidates", total)
col2.metric("Eligible", eligible)
col3.metric("Rejected", rejected)

st.divider()

st.subheader("💼 Job Description")
st.write(
    "Looking for AI/ML candidates with strong Python and Machine Learning skills."
)

st.subheader("⭐ Required Skills")
st.write("Python, Machine Learning")

st.divider()

if total == 0:
    st.info("No applications submitted yet. Go to the main page, analyze a resume, and click Apply Now.")

else:
    df = pd.DataFrame(applications)

    st.subheader("📊 Candidate Status Chart")
    st.bar_chart(df["Status"].value_counts())

    st.subheader("📈 Candidate Scores")
    st.bar_chart(df.set_index("Name")["Score"])

    st.subheader("📋 Recent Applications")

    search = st.text_input("Search Candidate")

    if search:
        df = df[
            df.apply(
                lambda row: search.lower() in row.astype(str).str.lower().to_string(),
                axis=1
            )
        ]

    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download CSV",
        data=csv_data,
        file_name="candidates.csv",
        mime="text/csv"
    )

    excel_file = "candidates.xlsx"
    df.to_excel(excel_file, index=False)

    with open(excel_file, "rb") as file:
        st.download_button(
            label="📊 Download Excel",
            data=file,
            file_name="candidates.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )