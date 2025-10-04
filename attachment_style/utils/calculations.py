import logging

import numpy as np

logger = logging.getLogger(__name__)


def revert_scores_for_reverted_questions(
        answers: dict[str, dict],
) -> dict[str, dict]:
    if len(answers) == 36:
        for key, value in answers.items():
            if value and value.get("question_text", {}).get("title", "").endswith("  **"):
                original_value = value  # for debugging
                reverted_value = {
                    "attachment_style": value["attachment_style"],
                    "score": abs(8 - value["score"]),
                    "question_text": value["question_text"],
                }
                # logger.info(f"reverting {original_value['value']} to {reverted_value['value']}")
                answers[key] = reverted_value

    return answers


def calculate_scores(
        answers: dict[str, dict],
) -> tuple[float, float, float]:
    anxious_vals = [
        answers[_]["score"] for _ in answers.keys() if answers[_] and answers[_]["attachment_style"] == "anxious"
    ]
    avoidant_vals = [
        answers[_]["score"] for _ in answers.keys() if answers[_] and answers[_]["attachment_style"] == "avoidant"
    ]
    anxious_score = np.average(anxious_vals) if anxious_vals else 0
    avoidant_score = np.average(avoidant_vals) if avoidant_vals else 0
    # secure_answers are empty for ecr-r (test yourself)
    secure_vals = [
        answers[_]["score"] for _ in answers.keys() if answers[_] and answers[_]["attachment_style"] == "secure"
    ]
    if secure_vals:
        secure_score = np.average(secure_vals)
    else:
        x_reverted = 4 - anxious_score
        y_reverted = 4 - avoidant_score
        diag_coord = (x_reverted + y_reverted) / 2
        secure_score = 4 + diag_coord

    return anxious_score, secure_score, avoidant_score


def calculate_kpis(df):
    total_submissions = len(df)

    anxious_total = 0
    avoidant_total = 0
    secure_total = 0

    for index, row in df.iterrows():
        if (row["anxious_score"] >= row["avoidant_score"]) and (row["anxious_score"] >= row["secure_score"]):
            anxious_total += 1
        if (row["avoidant_score"] >= row["anxious_score"]) and (row["avoidant_score"] >= row["secure_score"]):
            avoidant_total += 1
        if (row["secure_score"] >= row["avoidant_score"]) and (row["secure_score"] >= row["anxious_score"]):
            secure_total += 1

    if (secure_total >= avoidant_total) and (secure_total >= anxious_total):
        dominant_style_label = "Secure"
        dominant_style_percentage = round((secure_total / total_submissions)*100, 2)
    elif (anxious_total >= avoidant_total) and (anxious_total >= secure_total):
        dominant_style_label = "Anxious"
        dominant_style_percentage = round((anxious_total / total_submissions)*100, 2)
    else:
        dominant_style_percentage = round((avoidant_total / total_submissions)*100, 2)
        dominant_style_label = "Avoidant"

    male_len = len(df[df["gender"] == "male"])
    female_len = len(df[df["gender"] == "female"])
    other_len = len(df[df["gender"] == "other"])

    if (male_len >= female_len) and (male_len >= other_len):
        gender_label = "Male"
        gender_percentage = round((male_len / total_submissions)*100, 2)
    elif (other_len >= female_len) and (other_len >= male_len):
        gender_label = "Other"
        gender_percentage = round((other_len / total_submissions)*100, 2)
    else:
        gender_label = "Female"
        gender_percentage = round((female_len / total_submissions)*100, 2)

    extensive_len = len(df[df["therapy_experience"] == "extensive"])
    some_len = len(df[df["therapy_experience"] == "some"])
    none_len = len(df[df["therapy_experience"] == "none"])

    if (extensive_len >= some_len) and (extensive_len >= none_len):
        therapy_experience_label = "Extensive"
        therapy_experience_percentage = round((extensive_len / total_submissions)*100, 2)
    elif (none_len >= some_len) and (none_len >= extensive_len):
        therapy_experience_label = "None"
        therapy_experience_percentage = round((none_len / total_submissions)*100, 2)
    else:
        therapy_experience_label = "Some"
        therapy_experience_percentage = round((some_len / total_submissions)*100, 2)

    return (total_submissions, gender_label, gender_percentage, therapy_experience_label, therapy_experience_percentage,
            dominant_style_label, dominant_style_percentage)
