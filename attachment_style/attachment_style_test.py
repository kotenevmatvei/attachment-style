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
    sys.exit("Lists with questions must be the same length")

# Setup the lists to store the results
anxious_results: dict[str, int] = {}
secure_results: dict[str, int] = {}
avoidant_results: dict[str, int] = {}

# Explain the rules
print(
    "\nAnswer the following questions by entering a number between 0 and 10 "
    "indicating the extent to each statement applies to you.\n"
)


# Ask questions and store the results
def collect_answers(questions: list[str]) -> dict[str, float]:
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


anxious_results: dict[str, float] = collect_answers(anxious_questions)
secure_results: dict[str, float] = collect_answers(secure_questions)
avoidant_results: dict[str, float] = collect_answers(avoidant_questions)

# Calculate the score
anxious_score: float = sum(anxious_results.values())
secure_score: float = sum(secure_results.values())
avoidant_score: float = sum(avoidant_results.values())

# Build the plot
n: int = len(anxious_questions)  # length of the scala
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
plt.xlabel("Avoidance")
plt.title("Attachment Style Score")
plt.show()

# TODO random question selection