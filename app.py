import pandas as pd
from flask import (
    Flask,
    render_template,
    request,
    send_file,
    session,
    redirect,
    url_for
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from utils.parser import extract_text_from_pdf
from utils.skills import (
    extract_skills,
    missing_skills,
    suggest_improvements
)
from utils.matcher import calculate_match
from utils.database import db, Candidate

import os

app = Flask(__name__)

# SECRET KEY FOR LOGIN SESSION
app.config["SECRET_KEY"] = "resume_screening_secret_key_2026"
# -----------------------------
# Database Configuration
# -----------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///candidates.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# -----------------------------
# Upload Folder
# -----------------------------
UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# -----------------------------
# Database Initialization
# -----------------------------
db.init_app(app)

with app.app_context():
    db.create_all()


# =============================
# HOME PAGE
# =============================
@app.route("/")
def home():
    return render_template("index.html")


# =============================
# ANALYZE RESUME
# =============================
@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        # Candidate Details
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")

        # Company Requirements
        job_description = request.form.get(
            "job_description",
            "Python Machine Learning"
        )

        # Resume Upload
        resume_file = request.files["resume"]

        if resume_file.filename == "":
            return "Please upload a resume."

        # PDF Validation
        if not resume_file.filename.lower().endswith(".pdf"):
            return "Only PDF files are allowed."

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            resume_file.filename
        )

        resume_file.save(filepath)

        # Extract Resume Text
        resume_text = extract_text_from_pdf(filepath)

        # Extract Skills
        candidate_skills = extract_skills(
            resume_text
        )

        jd_skills = extract_skills(
            job_description
        )

        # Match Score
        score = calculate_match(
            candidate_skills,
            jd_skills
        )

        # Eligibility Status
        status = (
            "Eligible"
            if score >= 70
            else "Not Eligible"
        )

        # Missing Skills
        missing = missing_skills(
            candidate_skills,
            jd_skills
        )

        # Suggestions
        suggestions = suggest_improvements(
            missing
        )

        # Save Candidate
        candidate = Candidate(
            name=name,
            email=email,
            phone=phone,
            score=score,
            status=status
        )

        db.session.add(candidate)
        db.session.commit()

        return render_template(
            "result.html",
            name=name,
            email=email,
            phone=phone,
            score=score,
            status=status,
            candidate_skills=candidate_skills,
            missing=missing,
            suggestions=suggestions
        )

    except Exception as e:
        return f"Error: {str(e)}"


# =============================
# ADMIN LOGIN
# =============================
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":

            session["admin"] = True

            return redirect(url_for("admin"))

        return render_template(
            "admin_login.html",
            error="Invalid Username or Password"
        )

    return render_template("admin_login.html")


# =============================
# ADMIN DASHBOARD
# =============================
@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    candidates = Candidate.query.order_by(
        Candidate.score.desc()
    ).all()

    total = len(candidates)

    eligible = len(
        [c for c in candidates if c.status == "Eligible"]
    )

    rejected = total - eligible
    average_score = 0
    highest_score = 0
    success_rate = 0

    if total > 0:

        average_score = round(
            sum(c.score for c in candidates) / total,
            2
        )

        highest_score = max(
            c.score for c in candidates
        )

        success_rate = round(
            (eligible / total) * 100,
            2
        )


    return render_template(
    "admin.html",
    candidates=candidates,
    total=total,
    eligible=eligible,
    rejected=rejected,
    average_score=average_score,
    highest_score=highest_score,
    success_rate=success_rate
)


# =============================
# LOGOUT
# =============================
@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(url_for("admin_login"))

# =============================
# APPLY
# =============================
@app.route("/apply", methods=["POST"])
def apply():

    email = request.form.get("email")

    candidate = Candidate.query.filter_by(
        email=email
    ).first()

    if candidate:

        return """
        <h1 style='color:green;text-align:center;margin-top:50px;'>
        Application Submitted Successfully
        </h1>
        """

    return "Candidate Not Found"


# =============================
# PDF REPORT
# =============================
@app.route("/download_report/<name>/<int:score>")
def download_report(name, score):

    filename = os.path.join(
        app.config["REPORT_FOLDER"],
        f"{name}_report.pdf"
    )

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Resume Screening Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Candidate Name: {name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Match Score: {score}%",
            styles["Normal"]
        )
    )

    status = (
        "Eligible"
        if score >= 70
        else "Not Eligible"
    )

    content.append(
        Paragraph(
            f"Application Status: {status}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Generated by AI Resume Screening System",
            styles["Italic"]
        )
    )

    doc.build(content)

    return send_file(
        filename,
        as_attachment=True
    )
@app.route("/export_csv")
def export_csv():

    candidates = Candidate.query.all()

    data = []

    for c in candidates:
        data.append({
            "Name": c.name,
            "Email": c.email,
            "Phone": c.phone,
            "Score": c.score,
            "Status": c.status
        })

    df = pd.DataFrame(data)

    filename = "candidates.csv"

    df.to_csv(filename, index=False)

    return send_file(
        filename,
        as_attachment=True
    )

# =============================
# RUN APP
# =============================
if __name__ == "__main__":
    app.run(debug=True)