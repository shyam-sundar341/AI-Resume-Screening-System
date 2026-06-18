import spacy

nlp = spacy.load("en_core_web_sm")

skills_db = [
    "python",
    "java",
    "sql",
    "html",
    "css",
    "javascript",
    "machine learning",
    "deep learning",
    "nlp",
    "flask",
    "django",
    "tensorflow",
    "pytorch",
    "aws",
    "azure",
    "power bi",
    "excel"
]


def extract_skills(text):

    doc = nlp(text.lower())

    found = []

    for skill in skills_db:

        if skill in doc.text:
            found.append(skill)

    return list(set(found))


def missing_skills(candidate_skills, jd_skills):

    return list(
        set(jd_skills)
        - set(candidate_skills)
    )


def suggest_improvements(missing):

    suggestions = []

    for skill in missing:

        suggestions.append(
            f"Add projects and certifications related to {skill}"
        )

    return suggestions