# Imports
import sys
import matplotlib.pyplot as plt
import plotly.express as px
from utils import combine_and_shuffle_lists

def read_questions_file(questions_file_path: str, attachment_style: str) -> list[str]:
    """Read the txt file with questions and add them to the corresponding list."""
    questions_list: list[str] = []
    with open(questions_file_path, "r") as file:
        for line in file:
            questions_list.append((line.strip(), attachment_style))
            
    return questions_list

def check_same_length(
    anxious_questions: list[str],
    secure_questions: list[str],
    avoidant_questions: list[str]
    ) -> None:
    """Check if there is the same number of all types of questions."""
    
    list_same_length = (
        len(anxious_questions) == len(secure_questions) == len(avoidant_questions)
    )
    if not list_same_length:
        sys.exit("Lists with questions must be the same length")

def collect_answers(questions: list[tuple[str, str]]) -> dict[str, float]:
    """Ask questions and store the results in dictionaries. """
    
    answers: dict[str, list[str, float]] = {}
    for question, attachment_style in questions:
        input_valid = False
        while input_valid == False:
            try:
                answer = float(input(f"{question}:  "))
                if answer >= 0 and answer <= 10:
                    input_valid = True
                    answers[question] = (float(answer)/10, attachment_style)
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

def build_matplotlib_2d_plot(
    number_of_questions: int,
    anxious_score: float,
    secure_score: float,
    avoidant_score: float
) -> plt:
    
    n: int = number_of_questions  # length of the scala
    fig, ax = plt.subplots()  # Create a figure containing a single axes
    plt.xlim(0, 14)
    plt.ylim(0, 14)
    plt.grid(True)
    ax.set_xticks(list(range(0, 15)))
    ax.set_yticks(list(range(0, 15)))
    plt.axhline(7, color="brown", linewidth=1)
    plt.axvline(7, color="brown", linewidth=1)
    ax.scatter(anxious_score, avoidant_score)
    plt.gca().invert_yaxis()
    plt.tick_params(
        axis="x",
        which="both",
        bottom=False,
        top=True,
        labelbottom=False,
        labeltop=True,
    )
    plt.xlabel("Anxiety")
    plt.ylabel("Avoidance")
    plt.title("Attachment Style Score")
    
    return plt

def build_plotly_3d_plot(
    number_of_questions: int,
    anxious_score: list[float],
    secure_score: list[float],
    avoidant_score: list[float]
) -> px.scatter_3d:
    """Build a plotly 3d scatter figure"""
    fig = px.scatter_3d(
        x=anxious_score,
        y=secure_score, 
        z=avoidant_score,
        labels={
                "x": "Anxiety",
                "y": "Security",
                "z": "Avoidance"
        }
    )
    fig.update_layout(
    title = "Attachment Style Test",
    scene={
        "xaxis_title": 'Anxiety',
        "yaxis_title": 'Security',
        "zaxis_title": 'Avoidance',
        "xaxis": {"range": [0, 14]},
        "yaxis": {"range": [0, 14]},
        "zaxis": {"range": [0, 14]}
    }
)
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

# # setup the lists to store the results
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

# results: dict[str, tuple[float, str]] = collect_answers_at_random(
#     anxious_questions=anxious_questions,
#     secure_questions=secure_questions,
#     avoidant_questions=avoidant_questions
# )


