import pytest

from ..attachment_style.attachment_style_test import (
    read_questions_file,
    check_same_length,
    collect_answers,
    build_matplotlib_2d_plot
)

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

    # mock answers
    anxious_results: dict[str, float] = dict(zip())
    secure_results: dict[str, float] = collect_answers(secure_questions)
    avoidant_results: dict[str, float] = collect_answers(avoidant_questions)
    
    # calculate the score
    anxious_score: float = sum(anxious_results.values())
    secure_score: float = sum(secure_results.values())
    avoidant_score: float = sum(avoidant_results.values())
    
    # build the plot
    plot = build_matplotlib_2d_plot(
        number_of_questions=len(anxious_questions),
        anxious_score=anxious_score,
        secure_score=secure_score,
        avoidant_score=avoidant_score
    )
    
    plot.show()

if __name__ == "__main__":
    main()