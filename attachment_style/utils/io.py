import codecs
import json
import logging

logger = logging.getLogger(__name__)


def read_questions_file(
        questions_file_path: str, attachment_style: str
) -> list[dict]:
    """Read the txt file with questions and add them to the corresponding list.

    Returns a list of dicts with keys: question_text, attachment_style
    """
    questions_list: list[dict] = []
    with open(questions_file_path, "r") as file:
        for line in file:
            decoded_line = codecs.decode(line.strip(), "unicode_escape")
            line_with_reverse_score_accounted = decoded_line.replace(" /r/", "   ")
            questions_list.append({
                "question_text": line_with_reverse_score_accounted,
                "attachment_style": attachment_style,
            })

    return questions_list


def read_questions(subject: str) -> list[dict]:
    questions: list[dict] = []
    if subject == "you":
        questions.extend(
            read_questions_file(
                questions_file_path="data/ecr-r/anxious.txt",
                attachment_style="anxious",
            )
        )
        questions.extend(
            read_questions_file(
                questions_file_path="data/ecr-r/avoidant.txt",
                attachment_style="avoidant",
            )
        )
    else:
        questions.extend(
            read_questions_file(
                questions_file_path="data/partner/anxious.txt",
                attachment_style="anxious",
            )
        )
        questions.extend(
            read_questions_file(
                questions_file_path="data/partner/secure.txt", attachment_style="secure"
            )
        )
        questions.extend(
            read_questions_file(
                questions_file_path="data/partner/avoidant.txt",
                attachment_style="avoidant",
            )
        )
    return questions


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


