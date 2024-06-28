import plotly.express as px


def read_questions_file(questions_file_path: str, attachment_style: str) -> list[tuple[str, str]]:
    """Read the txt file with questions and add them to the corresponding list."""
    questions_list: list[tuple[str, str]] = []
    with open(questions_file_path, "r") as file:
        for line in file:
            questions_list.append((line.strip(), attachment_style))

    return questions_list


def calculate_scores(answers: dict[int, tuple[str, float]]) -> tuple[float,float, float]:
    anxious_score = sum(
        [
            answers[_][1]
            for _ in answers.keys()
            if answers[_][0] == "anxious"
        ]
    )
    secure_score = sum(
        [
            answers[_][1]
            for _ in answers.keys()
            if answers[_][0] == "secure"
        ]
    )
    avoidant_score = sum(
        [
            answers[_][1]
            for _ in answers.keys()
            if answers[_][0] == "avoidant"
        ]
    )
    return anxious_score, secure_score, avoidant_score


# build a pie chart
def build_pie_chart(
        anxious_score: float,
        secure_score: float,
        avoidant_score: float
) -> px.pie:
    # Create a list of labels and corresponding scores
    labels = ['Anxious', 'Secure', 'Avoidant']
    scores = [anxious_score, secure_score, avoidant_score]
    # Create the pie chart
    fig = px.pie(values=scores, names=labels, title='Attachment Style Pie Chart')
    # fig.update_layout(
    #     title_font={"size": 25},
    #     legend_font={"size": 25},
    #
    # )
    # # modify the font size
    # fig.update_traces(insidetextfont=dict(size=20))

    return fig


def generate_type_description(attachment_type: str) -> str:
    anxious_description = """
    Anxious: You love to be very close to your romantic partners and have the capacity 
    for great intimacy. You often fear, however, that your partner does not wish to be as 
    close as you would like him/her to be. Relationships tend to consume a large part of 
    your emotional energy. You tend to be very sensitive to small fluctuations in your 
    partner’s moods and actions, and although your senses are often accurate, you take 
    your partner’s behaviors too personally. You experience a lot of negative emotions 
    within the relationship and get easily upset. As a result, you tend to act out and 
    say things you later regret. If the other person provides a lot of security and 
    reassurance, however, you are able to shed much of your preoccupation and feel 
    contented.
    """
    secure_description = """
    Secure: Being warm and loving in a relationship comes naturally to you. You 
    enjoy being intimate without becoming overly worried about your relationships. 
    You take things in stride when it comes to romance and don’t get easily upset 
    over relationship matters. You effectively communicate your needs and feelings 
    to your partner and are strong at reading your partner’s emotional cues and 
    responding to them. You share your successes and problems with your mate, and 
    are able to be there for him or her in times of need.
    """
    avoidant_description = """
    Avoidant: It is very important for you to maintain your independence and 
    self-sufficiency and you often prefer autonomy to intimate relationships. Even 
    though you do want to be close to others, you feel uncomfortable with too much 
    closeness and tend to keep your partner at arm’s length. You don’t spend much 
    time  worrying about your romantic relationships or about being rejected. You 
    tend not to open up to your partners and they often complain that you are 
    emotionally distant. In relationships, you are often on high alert for any signs 
    of control or impingement on your territory by your partner.
    """
    match attachment_type:
        case "anxious":
            return anxious_description
        case "secure":
            return secure_description
        case "avoidant":
            return avoidant_description

# def check_same_length(
#         anxious_questions: list[str],
#         secure_questions: list[str],
#         avoidant_questions: list[str]
# ) -> None:
#     """Check if there is the same number of all types of questions."""
#
#     list_same_length = (
#             len(anxious_questions) == len(secure_questions) == len(avoidant_questions)
#     )
#     if not list_same_length:
#         sys.exit("Lists with questions must be the same length")

def read_questions() -> list[tuple[str, str]]:
    questions: list[tuple[str, str]] = []
    questions.extend(read_questions_file(questions_file_path="data/anxious_questions.txt", attachment_style="anxious"))
    questions.extend(read_questions_file(questions_file_path="data/secure_questions.txt", attachment_style="secure"))
    questions.extend(read_questions_file(questions_file_path="data/avoidant_questions.txt", attachment_style="avoidant"))
    return questions


# def combine_and_shuffle_lists(*lists):
#     combined_list = [item for sublist in lists for item in sublist]
#     random.shuffle(combined_list)
#     return combined_list
