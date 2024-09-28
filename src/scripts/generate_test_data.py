# generate test data and upload to the database

import random
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
from utils.utils import upload_to_db

# Define the number of test users and questions
NUM_USERS = 1000
NUM_QUESTIONS_YOURSELF = 42
NUM_QUESTIONS_PARTNER = 33

# Define possible answers and personal information
possible_answers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
relationship_statuses = ["single", "relationship", "married"]
genders = ["male", "female", "other"]
attachment_styles = ["secure", "anxious", "avoidant"]
therapy_experiences = ["none", "some", "extensive"]

# Generate random answers for the quiz
def generate_random_answers_yourself():
    answers = {}
    for i in range(NUM_QUESTIONS_YOURSELF):
        # question_id = f"question_{i+1}"
        answer = random.choice(possible_answers)
        attachment_style = random.choice(attachment_styles)
        answers[i] = (attachment_style, answer, "question_text")
    return answers

# Generate random answers for the quiz
def generate_random_answers_partner():
    answers = {}
    for i in range(NUM_QUESTIONS_PARTNER):
        # question_id = f"question_{i+1}"
        answer = random.choice(possible_answers)
        attachment_style = random.choice(attachment_styles)
        answers[i] = (attachment_style, answer, "question_text")
    return answers

# Generate random personal information
def generate_random_personal_info():
    age = random.randint(18, 70)
    relationship_status = random.choice(relationship_statuses)
    gender = random.choice(genders)
    therapy_experience = random.choice(therapy_experiences)
    personl_info = {
        "age": age,
        "relationship_status": relationship_status,
        "gender": gender,
        "therapy_experience": therapy_experience
    }
    return personl_info

# Main function to generate test data and upload to the database
def main():

    for _ in range(NUM_USERS):
        answers = generate_random_answers_yourself()
        personal_info = generate_random_personal_info()
        upload_to_db(answers, personal_info, test=True)

    for _ in range(NUM_USERS):
        answers = generate_random_answers_partner()
        personal_info = generate_random_personal_info()
        upload_to_db(answers, personal_info, test=True)
        
if __name__ == "__main__":
    main()