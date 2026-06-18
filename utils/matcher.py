def calculate_match(candidate_skills, jd_skills):

    if len(jd_skills) == 0:
        return 0

    matched_skills = set(candidate_skills).intersection(set(jd_skills))

    score = (len(matched_skills) / len(jd_skills)) * 100

    return round(score, 2)