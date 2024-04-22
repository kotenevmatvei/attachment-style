# Imports
import sys
import matplotlib.pyplot as plt

# Read the txt files with questions and build corresponding lists
anxious_questions: list[str] = []
secure_questions: list[str] = []
avoidant_questions: list[str] = []

# TODO Refactor to a function for improved modularity
with open("anxious_questions.txt", "r") as file:
    for line in file:
        anxious_questions.append(line.strip())
with open("secure_questions.txt", "r") as file:
    for line in file:
        secure_questions.append(line.strip())
with open("avoidant_questions.txt", "r") as file:
    for line in file:
        avoidant_questions.append(line.strip())

# Check for the same number of questions
list_same_length = (
    len(anxious_questions) == len(secure_questions) == len(avoidant_questions)
)
if not list_same_length:
    print(len(anxious_questions), len(secure_questions), len(avoidant_questions))
    sys.exit("Lists with questions must be the same length")

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

anxious_results: dict[str, int] = collect_answers(anxious_questions)
secure_results: dict[str, int] = collect_answers(secure_questions)
avoidant_results: dict[str, int] = collect_answers(avoidant_questions)

# Calculate the score
anxious_score: int = sum(anxious_results.values())
secure_score: int = sum(secure_results.values())
avoidant_score: int = sum(avoidant_results.values())

# Build the plot
n: int = len(anxious_questions) # length of the scala
fig, ax = plt.subplots()  # Create a figure containing a single axes
plt.xlim(0,14)
plt.ylim(0,14)
plt.grid(True)
ax.set_xticks(list(range(0,15)))
ax.set_yticks(list(range(0,15)))
plt.axhline(7, color='brown', linewidth=1)
plt.axvline(7, color='brown', linewidth=1) 
ax.scatter(anxious_score, avoidant_score)
plt.gca().invert_yaxis()
plt.tick_params(axis='x', which='both', bottom=False, top=True, 
                labelbottom=False, labeltop=True)
plt.savefig('plot0.png')
plt.xlabel("Anxiety")
plt.xlabel("Avoidance")
plt.title("Attachment Style Score")
plt.show()