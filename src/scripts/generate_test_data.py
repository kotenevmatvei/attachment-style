import numpy as np
from datetime import datetime
from psycopg2.extensions import register_adapter, AsIs
from src.models import TestYourself, TestYourPartner
from src.utils.utils import upload_objects_to_db

import random

register_adapter(np.int64, AsIs)
register_adapter(np.int32, AsIs)

# Define the number of test users and questions
NUM_TEST_YOURSELF = 1000
NUM_TEST_YOUR_PARTNER = 1000

# Define possible answers and personal information
possible_answers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
relationship_statuses = ["single", "relationship", "married"]
genders = ["male", "female", "other"]
attachment_styles = ["secure", "anxious", "avoidant"]
therapy_experiences = ["none", "some", "extensive"]


def generate_test_personal_info():
    rng = np.random.default_rng()
    gender = rng.choice(genders)
    age = rng.integers(18, 70, endpoint=True)
    relationship_status = rng.choice(relationship_statuses)
    therapy_experience = rng.choice(therapy_experiences)
    
    return gender, age, relationship_status, therapy_experience

def generate_test_scores(
    gender: str,
    age: int,
    relationship_status: str,
    therapy_experience: str,
    subject: str,
) -> tuple[np.array, np.array, np.array]:
    rng = np.random.default_rng()
    anxious_mean, secure_mean, avoidant_mean = 5, 5, 5
    # adjust means according to the (very rough) assumptions about population
    # gender
    if gender == "male":
        anxious_mean -= 1
        avoidant_mean += 1
    elif "female":
        anxious_mean += 1
        avoidant_mean -= 1
    # relationship_status
    if relationship_status == "married":
        secure_mean += 1
    # therapy_experience
    if therapy_experience == "some":
        secure_mean += 1
        anxious_mean -= 1
    elif therapy_experience == "extensive":
        avoidant_mean -= 2
        anxious_mean -= 2
        avoidant_mean -= 2
    # age
    if age > 50:
        secure_mean += 2
    elif age > 30:
        secure_mean += 2

    # set the standard deviations (~1/3 of the smaller interval)
    anxious_sigma = 0.33 * min(anxious_mean, 10 - anxious_mean)
    secure_sigma = 0.33 * min(secure_mean, 10 - secure_mean)
    avoidant_sigma = 0.33 * min(avoidant_mean, 10 - avoidant_mean)

    # generate scores
    n = 14 if subject == "you" else 11
    anxious_scores = np.rint(rng.normal(anxious_mean, anxious_sigma, n)).astype(int)
    secure_scores = np.rint(rng.normal(secure_mean, secure_sigma, n)).astype(int)
    avoidant_scores = np.rint(rng.normal(avoidant_mean, avoidant_sigma, n)).astype(int)

    return anxious_scores, secure_scores, avoidant_scores


def build_db_entry(
    gender: str,
    age: int,
    relationship_status: str,
    therapy_experience: str,
    subject: str,
    anxious_scores: np.array,
    secure_scores: np.array,
    avoidant_scores: np.array,
) -> TestYourPartner | TestYourself:
    
    n = 14 if subject == "you" else 11
    base_dict = {
        "timestamp": datetime.now(),
        "age": age,
        "gender": gender,
        "therapy_experience": therapy_experience,
        "relationship_status": relationship_status,
        "test": True
    }
    keys = [
        f"{style}_q{i}"
        for style in ("anxious", "secure", "avoidant")
        for i in range(1, n+1)
    ]
    values = np.concatenate((anxious_scores, secure_scores, avoidant_scores))
    scores_dict = dict(zip(keys, values))
    base_dict.update(scores_dict)

    if subject == "you":
        db_entry = TestYourself(**base_dict)
    elif subject == "parther":
        db_entry = TestYourPartner(**base_dict)
    else:
        raise ValueError(f"Unknown subject {subject}")
    
    return db_entry
    

def main(number_of_datapoints: int):
    db_entries = []
    for i in range(number_of_datapoints):
        gender, age, relationship_status, therapy_experience = generate_test_personal_info()
        anxious_scores, secure_scores, avoidant_scores = generate_test_scores(
            gender, age, relationship_status, therapy_experience, "you"
        )
        db_entry = build_db_entry(
            gender, age, relationship_status, therapy_experience, "you",
            anxious_scores, secure_scores, avoidant_scores
        )
        db_entries.append(db_entry)

    upload_objects_to_db(db_entries)

# Main function to generate test data and upload to the databas


if __name__ == "__main__":
    main(100)
