import codecs
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


