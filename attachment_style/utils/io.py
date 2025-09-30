import codecs
import json
import logging

logger = logging.getLogger(__name__)

def read_questions_file(
        questions_file_path: str, attachment_style: str
) -> list[tuple[str, str]]:
    """Read the txt file with questions and add them to the corresponding list."""
    questions_list: list[tuple[str, str]] = []
    with open(questions_file_path, "r") as file:
        for line in file:
            decoded_line = codecs.decode(line.strip(), "unicode_escape")
            line_with_reverse_score_accounted = decoded_line.replace(" /r/", "   ")
            questions_list.append((line_with_reverse_score_accounted, attachment_style))

    return questions_list


def read_questions(subject: str) -> list[tuple[str, str]]:
    questions: list[tuple[str, str]] = []
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
        return [(question, attachment_style) for question in data["questions"]]

def read_questions_json(subject):
    questions = []
    if subject == "others":
        questions.extend(read_questions_json_files("data/partner/anxious.json", "anxious"))
        questions.extend(read_questions_json_files("data/partner/secure.json", "secure"))
        questions.extend(read_questions_json_files("data/partner/avoidant.json", "avoidant"))
        print(questions)
        return questions
    else:
        questions.extend(read_questions_json_files("data/ecr-r/anxious.json", "anxious"))
        questions.extend(read_questions_json_files("data/ecr-r/anxious.json", "avoidant"))
        print(questions)
        return questions
