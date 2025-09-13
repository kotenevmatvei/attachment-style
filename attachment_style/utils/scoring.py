import logging
import numpy as np

logger = logging.getLogger(__name__)

def revert_scores_for_reverted_questions(
        answers: dict[str, tuple[str, float, str]],
) -> dict[str, tuple[str, float, str]]:
    if len(answers) == 36:
        for key, value in answers.items():
            if value[2].endswith("  **"):
                original_value = value  # for debugging
                reverted_value = (value[0], abs(8 - value[1]), value[2])
                logger.info(f"reverting {original_value[1]} to {reverted_value[1]}")
                answers[key] = reverted_value

    return answers


def calculate_scores(
        answers: dict[str, tuple[str, float, str]],
) -> tuple[float, float, float]:
    anxious_score = np.average(
        [answers[_][1] for _ in answers.keys() if answers[_][0] == "anxious"]
    )
    avoidant_score = np.average(
        [answers[_][1] for _ in answers.keys() if answers[_][0] == "avoidant"]
    )
    # secure_answers are empty for ecr-r (test yourself)
    secure_answers = [
        answers[_][1] for _ in answers.keys() if answers[_][0] == "secure"
    ]
    if secure_answers:
        secure_score = np.average(secure_answers)
    else:
        # x_and_y_coord = (anxious_score + avoidant_score) / 2
        # sign = np.sign(x_and_y_coord)
        # secure_score = np.sqrt(2 * (x_and_y_coord) ** 2) * sign
        x_reverted = 4 - anxious_score
        y_reverted = 4 - avoidant_score
        diag_coord = (x_reverted + y_reverted) / 2
        secure_score = 4 + diag_coord

    return anxious_score, secure_score, avoidant_score


