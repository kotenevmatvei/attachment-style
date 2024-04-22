# Imports
import matplotlib.pyplot as plt

# Read the txt files with questions and build corresponding lists
anxious_questions: list[str] = []
secure_questions: list[str] = []
avoidant_questions: list[str] = []

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
anxious_results: dict[str, int] = {}
secure_results: dict[str, int] = {}
avoidant_results: dict[str, int] ={}

# Explain the rules
print(
    "Answer the following questions by entering 1 for yes and 0 for 1.\n"
)

# Ask questions and store the results
def collect_answers(questions: list[str]) -> dict[str, int]:
    answers: dict[str, int] = {}
    for question in questions:
        input_valid = False
        while input_valid == False:
            answer = input(question)
            if answer == "0" or answer == "1":
                input_valid = True
                answers[question] = int(answer)
            else:
                print("Invalid input. Please enter 1 for yes and 0 for no")
    return answers

anxious_results = collect_answers(anxious_questions)
secure_results = collect_answers(secure_questions)
avoidant_results = collect_answers(avoidant_questions)

# Visualize
