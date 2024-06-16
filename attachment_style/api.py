# Imports
import sys
import matplotlib.pyplot as plt
import plotly.express as px
from attachment_style.utils.utils import combine_and_shuffle_lists

def collect_answers(questions: list[tuple[str, str]]) -> dict[str, float]:
    """Ask questions and store the results in dictionaries. """
    
    answers: list[dict[str, str|float]] = []
    for question, attachment_style in questions:
        input_valid = False
        while input_valid == False:
            try:
                score = float(input(f"{question}:  "))
                if score >= 0 and score <= 10:
                    input_valid = True
                    answers.append({"question": question, "attachment_style": attachment_style, "score": score/10})
                else:
                    print(
                        "Invalid input, the answer must greater than or equal "
                        "to 0 and less than or equal to 10."
                    )
            except ValueError:
                print("Invalid input. Please enter a number.")
    return answers

def collect_answers_at_random(
    #TODO not clear which answer belongs to which attachment style
    anxious_questions: list[str],
    secure_questions: list[str],
    avoidant_questions: list[str]
) -> dict[str]:
    all_questions = combine_and_shuffle_lists(
        anxious_questions,
        secure_questions,
        avoidant_questions
    )
    return collect_answers(all_questions) 

# build a pie chart
def build_pie_chart(
    anxious_score: list[float],
    secure_score: list[float],
    avoidant_score: list[float]
) -> px.pie:
    
    # Create a list of labels and corresponding scores
    labels = ['Anxious', 'Secure', 'Avoidant']
    scores = [sum(anxious_score), sum(secure_score), sum(avoidant_score)]
    # Create the pie chart
    fig = px.pie(values=scores, names=labels, title='Attachment Style Pie Chart')

    return fig
    
# # read question files
# anxious_questions: list[tuple[str, str]] = read_questions_file("anxious_questions.txt", "anxious")
# secure_questions: list[tuple[str, str]] = read_questions_file("secure_questions.txt", "secure")
# avoidant_questions: list[tuple[str, str]] = read_questions_file("avoidant_questions.txt", "avoidant")

# # check that there is the same number of questions
# check_same_length(
#     anxious_questions=anxious_questions,
#     secure_questions=secure_questions,
#     avoidant_questions=avoidant_questions
# )

# # Setup the lists to store the results
# anxious_results: dict[str, int] = {}
# secure_results: dict[str, int] = {}
# avoidant_results: dict[str, int] = {}

# # explain the rules
# print(
#     "\nAnswer the following questions by entering a number between 0 and 10 "
#     "indicating the extent to each statement applies to you.\n"
# )

# # collect answers
# anxious_results: dict[str, float] = collect_answers(anxious_questions)
# secure_results: dict[str, float] = collect_answers(secure_questions)
# avoidant_results: dict[str, float] = collect_answers(avoidant_questions)

# # results: dict[str, tuple[float, str]] = collect_answers_at_random(
# #     anxious_questions=anxious_questions,
# #     secure_questions=secure_questions,
# #     avoidant_questions=avoidant_questions
# # )


