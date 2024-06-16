# import sys

def read_questions_file(questions_file_path: str, attachment_style: str) -> list[tuple[str, str]]:
    """Read the txt file with questions and add them to the corresponding list."""
    questions_list: list[tuple[str, str]] = []
    with open(questions_file_path, "r") as file:
        for line in file:
            questions_list.append((line.strip(), attachment_style))

    return questions_list

# def check_same_length(
#         anxious_questions: list[str],
#         secure_questions: list[str],
#         avoidant_questions: list[str]
# ) -> None:
#     """Check if there is the same number of all types of questions."""
#
#     list_same_length = (
#             len(anxious_questions) == len(secure_questions) == len(avoidant_questions)
#     )
#     if not list_same_length:
#         sys.exit("Lists with questions must be the same length")

def read_questions() -> list[tuple[str, str]]:
    questions: list[tuple[str, str]] = []
    questions.extend(read_questions_file(questions_file_path="data/anxious_questions.txt", attachment_style="anxious"))
    questions.extend(read_questions_file(questions_file_path="data/secure_questions.txt", attachment_style="secure"))
    questions.extend(read_questions_file(questions_file_path="data/avoidant_questions.txt", attachment_style="avoidant"))
    return questions


# def combine_and_shuffle_lists(*lists):
#     combined_list = [item for sublist in lists for item in sublist]
#     random.shuffle(combined_list)
#     return combined_list
