import numpy as np
import logging
import time
import sys
from datetime import datetime

import pandas as pd
from psycopg2.extensions import register_adapter, AsIs
from models import AssessYourself, AssessOthers
from utils.io import upload_objects_to_db

register_adapter(np.int64, AsIs)
register_adapter(np.int32, AsIs)

logging.basicConfig(
    level=logging.INFO,
    # format="{asctime} - {levelname} - {filename} - {funcName} - {message}",
    format="APP: {levelname} - {filename} - {funcName} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

# define the constants
NUM_DATAPOINTS = 100
SIGMA = 1.5
MEAN_INITIAL = 5
MEAN_INCREMENT = 0.5
NUMBER_OF_QUESTIONS_ASSESS_YOURSELF = 18
NUMBER_OF_QUESTIONS_ASSESS_OTHERS = 11

# define possible answers and personal information
possible_answers = [1, 2, 3, 4, 5, 6, 7]
relationship_statuses = ["single", "in_relationship", "married"]
genders = ["male", "female", "other"]
attachment_styles = ["secure", "anxious", "avoidant"]
therapy_experiences = ["none", "some", "extensive"]
subjects = ["you", "others"]

rng = np.random.default_rng(42)


def generate_test_personal_info():
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
    anxious_mean, avoidant_mean, secure_mean = adjust_means(
        age, gender, relationship_status, therapy_experience
    )

    # generate scores
    n = (
        NUMBER_OF_QUESTIONS_ASSESS_YOURSELF
        if subject == "you"
        else NUMBER_OF_QUESTIONS_ASSESS_OTHERS
    )
    anxious_scores = np.clip(
        np.rint(rng.normal(anxious_mean, SIGMA, n)).astype(int), 1, 7
    )
    secure_scores = np.clip(
        np.rint(rng.normal(secure_mean, SIGMA, n)).astype(int), 1, 7
    )
    avoidant_scores = np.clip(
        np.rint(rng.normal(avoidant_mean, SIGMA, n)).astype(int), 1, 7
    )

    return anxious_scores, secure_scores, avoidant_scores


def adjust_means(
    age: int, gender: str, relationship_status: str, therapy_experience: str
) -> tuple[float, float, float]:
    anxious_mean, secure_mean, avoidant_mean = (
        MEAN_INITIAL,
        MEAN_INITIAL,
        MEAN_INITIAL,
    )
    # adjust means according to the (very rough) assumptions about population
    # gender
    if gender == "male":
        anxious_mean -= MEAN_INCREMENT
        avoidant_mean += MEAN_INCREMENT
    elif gender == "female":
        anxious_mean += MEAN_INCREMENT
        avoidant_mean -= MEAN_INCREMENT
    # relationship_status
    if relationship_status == "in_relationship":
        anxious_mean -= MEAN_INCREMENT
        secure_mean += MEAN_INCREMENT
        avoidant_mean -= MEAN_INCREMENT
    elif relationship_status == "married":
        anxious_mean -= 2 * MEAN_INCREMENT
        secure_mean += 2 * MEAN_INCREMENT
        avoidant_mean -= 2 * MEAN_INCREMENT
    # therapy_experience
    if therapy_experience == "some":
        anxious_mean -= MEAN_INCREMENT
        secure_mean += MEAN_INCREMENT
        avoidant_mean -= MEAN_INCREMENT
    elif therapy_experience == "extensive":
        anxious_mean -= 2 * MEAN_INCREMENT
        secure_mean += 2 * MEAN_INCREMENT
        avoidant_mean -= 2 * MEAN_INCREMENT
    # age
    if age > 50:
        secure_mean += 2 * MEAN_INCREMENT
    elif age > 30:
        secure_mean += MEAN_INCREMENT
    return anxious_mean, avoidant_mean, secure_mean


def build_db_entry(
    gender: str,
    age: int,
    relationship_status: str,
    therapy_experience: str,
    subject: str,
    anxious_scores: np.array,
    secure_scores: np.array,
    avoidant_scores: np.array,
) -> AssessOthers | AssessYourself:
    n = 18 if subject == "you" else 11
    if subject == "others":
        n = 11
        base_dict = {
            "timestamp": datetime.utcnow(),
            "age": age,
            "gender": gender,
            "therapy_experience": therapy_experience,
            "relationship_status": relationship_status,
            "test": True,
        }

        scores_dict = {
            f"{style}_q{i}": score
            for style, scores in zip(
                ("anxious", "secure", "avoidant"),
                (anxious_scores, secure_scores, avoidant_scores),
            )
            for i, score in enumerate(scores, 1)
        }
        base_dict.update(scores_dict)

        db_entry = AssessOthers(**base_dict)

    elif subject == "you":
        n = 18
        base_dict = {
            "timestamp": datetime.utcnow(),
            "age": age,
            "gender": gender,
            "therapy_experience": therapy_experience,
            "relationship_status": relationship_status,
            "test": True,
        }

        scores_dict = {
            f"{style}_q{i}": score
            for style, scores in zip(
                ("anxious", "avoidant"),
                (anxious_scores, avoidant_scores),
            )
            for i, score in enumerate(scores, 1)
        }
        base_dict.update(scores_dict)

        db_entry = AssessYourself(**base_dict)
    
    else:
        raise ValueError("Unknown subject... ")
    

    return db_entry


def main(num_datapoints: int):
    logger = logging.getLogger(__name__)
    for subject in subjects:
        db_entries = []
        start_time = time.time()
        for i in range(num_datapoints):
            gender, age, relationship_status, therapy_experience = (
                generate_test_personal_info()
            )
            anxious_scores, secure_scores, avoidant_scores = generate_test_scores(
                gender, age, relationship_status, therapy_experience, subject
            )
            db_entry = build_db_entry(
                gender,
                age,
                relationship_status,
                therapy_experience,
                subject,
                anxious_scores,
                secure_scores,
                avoidant_scores,
            )
            db_entries.append(db_entry)
        elapsed_time = time.time() - start_time
        start_time = time.time()
        upload_objects_to_db(db_entries)
        elapsed_time = time.time() - start_time
        logger.info(f"Uploaded {NUM_DATAPOINTS} test datapoints for {subject}  to db in {elapsed_time}s")


if __name__ == "__main__":
    main(NUM_DATAPOINTS)
