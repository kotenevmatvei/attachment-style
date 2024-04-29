# Imports
import sys
import matplotlib.pyplot as plt

def read_questions_file(questions_file: str) -> list[str]:
    """Read the txt file with questions and add them to the corresponding list.

    :param questions_file: Path to the file with questions
    :return: question_list List with questions #TODO variable name in ruturn?
    """
    questions_list: list[str] = []
    with open(questions_file, "r") as file:
        for line in file:
            questions_list.append(line.strip())
            
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

def collect_answers(questions: list[str]) -> dict[str, float]:
    """Ask questions and store the results in dictionaries. """
    
    answers: dict[str, float] = {}
    for question in questions:
        input_valid = False
        while input_valid == False:
            try:
                answer = float(input(f"{question}:  "))
                if answer >= 0 and answer <= 10:
                    input_valid = True
                    answers[question] = float(answer)/10
                else:
                    print(
                        "Invalid input, the answer must greater than or equal "
                        "to 0 and less than or equal to 10."
                    )
            except ValueError:
                print("Invalid input. Please enter a number.")
    return answers

def build_plot(
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
    plt.savefig("plot0.png")
    plt.xlabel("Anxiety")
    plt.ylabel("Avoidance")
    plt.title("Attachment Style Score")
    
    return plt


# TODO random question selection
# TODO 3d plot - use plotly (and than dash!!)


def main() -> None:
    # read question files
    anxious_questions: list[str] = read_questions_file("anxious_questions.txt")
    secure_questions: list[str] = read_questions_file("secure_questions.txt")
    avoidant_questions: list[str] = read_questions_file("avoidant_questions.txt")
    
    # check that there is the same number of questions
    check_same_length(
        anxious_questions=anxious_questions,
        secure_questions=secure_questions,
        avoidant_questions=avoidant_questions
    )
    
    # setup the lists to store the results
    # Setup the lists to store the results
    anxious_results: dict[str, int] = {}
    secure_results: dict[str, int] = {}
    avoidant_results: dict[str, int] = {}
    
    # explain the rules
    print(
        "\nAnswer the following questions by entering a number between 0 and 10 "
        "indicating the extent to each statement applies to you.\n"
    )

    # collect answers
    anxious_results: dict[str, float] = collect_answers(anxious_questions)
    secure_results: dict[str, float] = collect_answers(secure_questions)
    avoidant_results: dict[str, float] = collect_answers(avoidant_questions)
    
    # calculate the score
    anxious_score: float = sum(anxious_results.values())
    secure_score: float = sum(secure_results.values())
    avoidant_score: float = sum(avoidant_results.values())
    
    # build the plot
    plot = build_plot(
        number_of_questions=len(anxious_questions),
        anxious_score=anxious_score,
        secure_score=secure_score,
        avoidant_score=avoidant_score
    )
    
    plot.show()

if __name__ == "__main__":
    main()