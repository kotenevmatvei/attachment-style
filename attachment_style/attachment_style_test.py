# Imports
import matplotlib.pyplot as plt

# Read the txt files with questions and build corresponding lists
anxious_questions = []
secure_questions = []
avoidant_questions = []
with open("anxious_questions.txt", "r") as f:
    for i in range(13):
        anxious_questions.append(f.readline()[:-1]) # Cut off the \n at the end
with open("secure_questions.txt", "r") as f:
    for i in range(13):
        secure_questions.append(f.readline()[:-1])
with open("avoidant_questions.txt", "r") as f:
    for i in range(13):
        avoidant_questions.append(f.readline()[:-1])


# Setup the lists to store the results
anxious_results = [0]*14
secure_results = [0]*14
avoidant_results =[0]*14

# Ask questions and store the results


# Visualize
