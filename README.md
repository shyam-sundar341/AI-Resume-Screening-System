# AI-Powered Resume Screening System

## Overview

The AI-Powered Resume Screening System is a Flask-based web application that helps recruiters and companies automate the initial resume screening process.

The system analyzes candidate resumes, extracts relevant skills using NLP techniques, compares them against company job requirements, calculates a match percentage, identifies missing skills, provides improvement suggestions, ranks candidates, and generates downloadable PDF reports.

---

## Features

### Candidate Portal

* Upload Resume (PDF Format)
* Enter Candidate Details

  * Name
  * Email
  * Phone Number
* AI-Based Resume Analysis
* Match Score Calculation
* Skill Extraction
* Missing Skill Identification
* Improvement Suggestions
* Eligibility Check
* Apply Now Functionality
* PDF Report Download

### Recruiter Dashboard

* View All Candidates
* Candidate Ranking System
* Statistics Dashboard
* Eligible vs Rejected Candidates
* Candidate Score Tracking
* Candidate Database Storage

---

## Technologies Used

### Frontend

* HTML5
* CSS3
* Bootstrap 5

### Backend

* Python
* Flask

### Database

* SQLite
* Flask-SQLAlchemy

### NLP & Resume Processing

* PDFPlumber
* Natural Language Processing (NLP)

### Reporting

* ReportLab

---

## Project Architecture

```text
resume_screening_system/
│
├── app.py
├── requirements.txt
├── candidates.db
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── admin.html
│
├── utils/
│   ├── parser.py
│   ├── skills.py
│   ├── matcher.py
│   └── database.py
│
├── uploads/
│
└── README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/resume-screening-system.git

cd resume-screening-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Workflow

1. Candidate enters personal details.
2. Candidate uploads resume.
3. System extracts text from PDF.
4. Skills are identified using NLP.
5. Skills are compared with company requirements.
6. Match percentage is calculated.
7. Missing skills are identified.
8. Suggestions are generated.
9. Candidate eligibility is determined.
10. Recruiters can view rankings and analytics.
11. PDF report can be downloaded.

---

## Sample Company Requirements

### Required Skills

* Python
* Machine Learning

### Responsibilities

* Build AI Applications
* Develop ML Models

---

## Future Enhancements

* spaCy NLP Integration
* Resume Ranking using Machine Learning
* Multiple Job Profiles
* Email Notifications
* Admin Authentication
* Cloud Deployment
* Resume Parsing using Advanced NLP
* Export Candidate Data to Excel
* Real-Time Analytics Dashboard

---

## Learning Outcomes

This project demonstrates practical implementation of:

* Python Full Stack Development
* Flask Web Development
* Database Integration
* Natural Language Processing
* Resume Parsing
* Data Analysis
* Recruiter Automation
* Software Engineering Practices

---

## Author

**Shyam**

B.Tech – Artificial Intelligence & Machine Learning

ServiceNow Certified System Administrator (CSA)

Aspiring AI/ML Engineer

---

## License

This project is developed for educational and portfolio purposes.
