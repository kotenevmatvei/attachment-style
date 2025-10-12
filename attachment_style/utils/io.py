import codecs
import json
import logging

logger = logging.getLogger(__name__)


def read_questions_json_files(file_path, attachment_style):
    with open(file_path) as file:
        data = json.load(file)
        return [{"question_text": question, "attachment_style": attachment_style} for question in data["questions"]]


def read_questions_json(subject):
    questions = []
    if subject == "others":
        questions.extend(read_questions_json_files("data/partner/anxious.json", "anxious"))
        questions.extend(read_questions_json_files("data/partner/secure.json", "secure"))
        questions.extend(read_questions_json_files("data/partner/avoidant.json", "avoidant"))
        return questions
    else:
        questions.extend(read_questions_json_files("data/ecr-r/anxious.json", "anxious"))
        questions.extend(read_questions_json_files("data/ecr-r/avoidant.json", "avoidant"))
        for question in questions:
            # we don't want /r/ to be visible in the app, so we leave some trailing spaces to know later that the score
            # is to be reverted
            question["question_text"]["title"] = question["question_text"]["title"].replace(" /r/", "   ")

        return questions


