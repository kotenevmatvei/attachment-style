import csv
import random
import numpy as np

SCORE_OPTIONS = [1, 2, 3, 4, 5, 6, 7]
NUMBER_OF_QUESTIONS = 18
NUMBER_OF_CASES = 50
ANXIOUS_REVERSED_QUESTION_INDS = [8, 10]
AVOIDANT_REVERSED_QUESTION_INDS = [1, 3, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17]

# generate and write
anxious_scores = []
avoidant_scores = []
with open("correct_scores_before_revert.csv", "a") as f:
    writer = csv.writer(f)
    for case_ind in range(NUMBER_OF_CASES):
        anxious_case_scores = []
        avoidant_case_scores = []

        for question_ind in range(NUMBER_OF_QUESTIONS):

            anxious_score = random.choice(SCORE_OPTIONS)
            anxious_case_scores.append(anxious_score)

            avoidant_score = random.choice(SCORE_OPTIONS)
            avoidant_case_scores.append(avoidant_score)

        row = anxious_case_scores + avoidant_case_scores
        writer.writerow(row)

        anxious_scores.append(anxious_case_scores)
        avoidant_scores.append(avoidant_case_scores)


# revert scores that need to be
with open("correct_scores_after_revert.csv", "a") as f:
    writer = csv.writer(f)
    for case_ind in range(NUMBER_OF_CASES):

        for question_ind in ANXIOUS_REVERSED_QUESTION_INDS:
            anxious_scores[case_ind][question_ind] = 8 - anxious_scores[case_ind][question_ind]

        for question_ind in AVOIDANT_REVERSED_QUESTION_INDS:
            avoidant_scores[case_ind][question_ind] = 8 - avoidant_scores[case_ind][question_ind]
        
        row = anxious_scores[case_ind] + avoidant_scores[case_ind]
        writer.writerow(row)




# calculate averages
with open("correct_averages.csv", "a") as f:
    writer = csv.writer(f)
    for case_ind in range(NUMBER_OF_CASES):

        anxious_average = np.average(anxious_scores[case_ind])
        avoidant_average = np.average(avoidant_scores[case_ind])

        row = [round(anxious_average, 2), round(avoidant_average, 2)]
        writer.writerow(row)

