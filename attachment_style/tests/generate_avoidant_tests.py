import random
import numpy as np

SCORE_OPTIONS = [1, 2, 3, 4, 5, 6, 7]
NUMBER_OF_QUESTIONS = 18
NUMBER_OF_CASES = 11
REVERSED_QUESTION_INDS = [1, 3, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17]

scores = []
for case_ind in range(NUMBER_OF_CASES):
    case_scores = []
    for question_ind in range(NUMBER_OF_QUESTIONS):
        score = random.choice(SCORE_OPTIONS)
        case_scores.append(score)
    scores.append(case_scores)

# reverse scores
for case_ind in range(NUMBER_OF_CASES):
    for question_ind in REVERSED_QUESTION_INDS:
        scores[case_ind][question_ind] = 8 - scores[case_ind][question_ind]


averages = []
for case_ind in range(NUMBER_OF_CASES):
    average = np.average(scores[case_ind])
    averages.append(average)

for case_ind in range(NUMBER_OF_CASES):
    print("scores: ", scores[case_ind])
    print("average: ", averages[case_ind])

