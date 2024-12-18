import plotly.express as px
import pandas as pd
import numpy as np
import os
import codecs
from sqlalchemy.orm import Session
from datetime import datetime as dt
from datetime import timedelta
from models import (
    Base,
    TestYourself,
    TestYourPartner,
)  # import works while utils imported in app.py
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv("../../.env")



# production url
url = str(os.getenv("DB_URL"))
url = "postgresql://koyeb-adm:DsanX26eJSmM@ep-autumn-pond-a2sga02t.eu-central-1.pg.koyeb.app/koyebdb"
url = "postgresql://avnadmin:AVNS_hppOVDRplQceY1kcoEA@attachment-style-attachment-style.f.aivencloud.com:17403/defaultdb?sslmode=require"

# dev url
# url = "postgresql://postgres:password@localhost:32772/"

engine = create_engine(url=url)


def read_questions_file(
    questions_file_path: str, attachment_style: str
) -> list[tuple[str, str]]:
    """Read the txt file with questions and add them to the corresponding list."""
    questions_list: list[tuple[str, str]] = []
    with open(questions_file_path, "r") as file:
        for line in file:
            decoded_line = codecs.decode(line.strip(), "unicode_escape")
            questions_list.append((decoded_line, attachment_style))

    return questions_list


def calculate_scores(
    answers: dict[int, tuple[str, float]],
) -> tuple[float, float, float]:
    anxious_score = sum(
        [answers[_][1] for _ in answers.keys() if answers[_][0] == "anxious"]
    )
    secure_score = sum(
        [answers[_][1] for _ in answers.keys() if answers[_][0] == "secure"]
    )
    avoidant_score = sum(
        [answers[_][1] for _ in answers.keys() if answers[_][0] == "avoidant"]
    )
    return anxious_score, secure_score, avoidant_score


# build a pie chart
def build_pie_chart(
    anxious_score: float, secure_score: float, avoidant_score: float
) -> px.pie:
    # Create a list of labels and corresponding scores
    labels = ["Anxious", "Secure", "Avoidant"]
    scores = [anxious_score, secure_score, avoidant_score]
    # Create the pie chart
    fig = px.pie(values=scores, names=labels, title="Attachment Style Pie Chart")

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


def read_questions(subject: str) -> list[tuple[str, str]]:
    questions: list[tuple[str, str]] = []
    if subject == "you":
        questions.extend(
            read_questions_file(
                questions_file_path="data/anxious_questions.txt",
                attachment_style="anxious",
            )
        )
        questions.extend(
            read_questions_file(
                questions_file_path="data/secure_questions.txt",
                attachment_style="secure",
            )
        )
        questions.extend(
            read_questions_file(
                questions_file_path="data/avoidant_questions.txt",
                attachment_style="avoidant",
            )
        )
    else:
        questions.extend(
            read_questions_file(
                questions_file_path="data/anxious_partner.txt",
                attachment_style="anxious",
            )
        )
        questions.extend(
            read_questions_file(
                questions_file_path="data/secure_partner.txt", attachment_style="secure"
            )
        )
        questions.extend(
            read_questions_file(
                questions_file_path="data/avoidant_partner.txt",
                attachment_style="avoidant",
            )
        )
    return questions


def increase_figure_font(fig: px.pie) -> None:
    # adjust font for the figure
    fig.update_layout(
        title_font={"size": 25},
        legend_font={"size": 25},
    )
    # modify the font size
    fig.update_traces(insidetextfont={"size": 20}, outsidetextfont={"size": 20})


def upload_to_db(
    answers: dict[str, tuple[str, float, str]],
    personal_answers: dict[str, str],
    test: bool = False,
):
    anxious_answers = sorted(
        [(value[2], value[1]) for value in answers.values() if value[0] == "anxious"]
    )
    secure_answers = sorted(
        [(value[2], value[1]) for value in answers.values() if value[0] == "secure"]
    )
    avoidant_answers = sorted(
        [(value[2], value[1]) for value in answers.values() if value[0] == "avoidant"]
    )
    values = []
    values.extend([value[1] for value in anxious_answers])
    values.extend([value[1] for value in secure_answers])
    values.extend([value[1] for value in avoidant_answers])

    if len(values) == 42:
        result_object = TestYourself(
            timestamp=dt.now() + timedelta(hours=2),
            test=test,
            age=personal_answers["age"],
            relationship_status=personal_answers["relationship_status"],
            gender=personal_answers["gender"],
            therapy_experience=personal_answers["therapy_experience"],
            anxious_q1=values[0],
            anxious_q2=values[1],
            anxious_q3=values[2],
            anxious_q4=values[3],
            anxious_q5=values[4],
            anxious_q6=values[5],
            anxious_q7=values[6],
            anxious_q8=values[7],
            anxious_q9=values[8],
            anxious_q10=values[9],
            anxious_q11=values[10],
            anxious_q12=values[11],
            anxious_q13=values[12],
            anxious_q14=values[13],
            secure_q1=values[14],
            secure_q2=values[15],
            secure_q3=values[16],
            secure_q4=values[17],
            secure_q5=values[18],
            secure_q6=values[19],
            secure_q7=values[20],
            secure_q8=values[21],
            secure_q9=values[22],
            secure_q10=values[23],
            secure_q11=values[24],
            secure_q12=values[25],
            secure_q13=values[26],
            secure_q14=values[27],
            avoidant_q1=values[28],
            avoidant_q2=values[29],
            avoidant_q3=values[30],
            avoidant_q4=values[31],
            avoidant_q5=values[32],
            avoidant_q6=values[33],
            avoidant_q7=values[34],
            avoidant_q8=values[35],
            avoidant_q9=values[36],
            avoidant_q10=values[37],
            avoidant_q11=values[38],
            avoidant_q12=values[39],
            avoidant_q13=values[40],
            avoidant_q14=values[41],
        )
    elif len(values) == 33:
        result_object = TestYourPartner(
            timestamp=dt.now() + timedelta(hours=2),
            test=test,
            age=personal_answers["age"],
            relationship_status=personal_answers["relationship_status"],
            gender=personal_answers["gender"],
            therapy_experience=personal_answers["therapy_experience"],
            anxious_q1=values[0],
            anxious_q2=values[1],
            anxious_q3=values[2],
            anxious_q4=values[3],
            anxious_q5=values[4],
            anxious_q6=values[5],
            anxious_q7=values[6],
            anxious_q8=values[7],
            anxious_q9=values[8],
            anxious_q10=values[9],
            anxious_q11=values[10],
            secure_q1=values[11],
            secure_q2=values[12],
            secure_q3=values[13],
            secure_q4=values[14],
            secure_q5=values[15],
            secure_q6=values[16],
            secure_q7=values[17],
            secure_q8=values[18],
            secure_q9=values[19],
            secure_q10=values[20],
            secure_q11=values[21],
            avoidant_q1=values[22],
            avoidant_q2=values[23],
            avoidant_q3=values[24],
            avoidant_q4=values[25],
            avoidant_q5=values[26],
            avoidant_q6=values[27],
            avoidant_q7=values[28],
            avoidant_q8=values[29],
            avoidant_q9=values[30],
            avoidant_q10=values[31],
            avoidant_q11=values[32],
        )
    else:
        raise ValueError("The number of answers is not correct")

    with Session(engine) as session:
        session.add(result_object)
        session.commit()


# get data from the database
def get_data_from_db(test: bool = True):
    with Session(engine) as session:
        test_yourself = (
            session.query(TestYourself).filter(TestYourself.test == test).all()
        )
        test_your_partner = (
            session.query(TestYourPartner).filter(TestYourPartner.test == test).all()
        )
        # Convert query results to DataFrame
        test_yourself_df = pd.DataFrame(
            [
                dict(
                    sorted(
                        {
                            k: v
                            for k, v in t.__dict__.items()
                            if k != "_sa_instance_state"
                        }.items()
                    )
                )
                for t in test_yourself
            ]
        )
        test_your_partner_df = pd.DataFrame(
            [
                dict(
                    sorted(
                        {
                            k: v
                            for k, v in t.__dict__.items()
                            if k != "_sa_instance_state"
                        }.items()
                    )
                )
                for t in test_your_partner
            ]
        )

        session.commit()
        return test_yourself_df, test_your_partner_df


def aggregate_scores(test_yourself_df, test_your_partner_df):
    # calculate scores
    # Add a column with the sum of all columns starting with "anxious"
    test_yourself_df["anxious_score"] = (
        test_yourself_df.filter(like="anxious").sum(axis=1) / 14
    )
    test_your_partner_df["anxious_score"] = (
        test_your_partner_df.filter(like="anxious").sum(axis=1) / 11
    )
    # Add a column with the sum of all columns starting with "secure"
    test_yourself_df["secure_score"] = (
        test_yourself_df.filter(like="secure").sum(axis=1) / 14
    )
    test_your_partner_df["secure_score"] = (
        test_your_partner_df.filter(like="secure").sum(axis=1) / 11
    )
    # Add a column with the sum of all columns starting with "avoidant"
    test_yourself_df["avoidant_score"] = (
        test_yourself_df.filter(like="avoidant").sum(axis=1) / 14
    )
    test_your_partner_df["avoidant_score"] = (
        test_your_partner_df.filter(like="avoidant").sum(axis=1) / 11
    )

    return test_yourself_df, test_your_partner_df


# create 3d chart
def create_3d_chart(test_yourself, test_your_partner, subject, symbol_parameter):
    # create a 3d chart
    # symbol_parameter can be "gender" or "relationship_status" or "therapy_experience"
    if subject == "you":
        fig = px.scatter_3d(
            test_yourself,
            x="anxious_score",
            y="secure_score",
            z="avoidant_score",
            color="age",
            symbol=symbol_parameter,
        )
    else:
        fig = px.scatter_3d(
            test_your_partner,
            x="anxious_score",
            y="secure_score",
            z="avoidant_score",
            color="age",
            symbol=symbol_parameter,
        )

    # modify axes length
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 12]),
            yaxis=dict(range=[0, 12]),
            zaxis=dict(range=[0, 12]),
        )
    )

    # make the figure wider
    fig.update_layout(width=800)

    # adjust legend positions
    fig.update_layout(
        legend=dict(
            x=0,  # x position of the legend
            y=1,  # y position of the legend
        )
    )

    # make symbols smaller
    # fig.update_traces(marker=dict(size=4))

    return fig


def generate_test_data_stupid_chargpt():
    # Set a random seed for reproducibility
    np.random.seed(42)

    # Number of data points
    n = 100

    # Age distribution: Normal distribution around 30 years with a standard deviation of 8, clipped between 18 and 65
    ages = np.clip(np.random.normal(loc=30, scale=8, size=n), 18, 65).astype(int)

    # Therapy experience distribution
    therapy_experience_options = ["None", "Some", "Extensive"]
    therapy_experience_probs = [0.5, 0.3, 0.2]  # 50% None, 30% Some, 20% Extensive
    therapy_experience = np.random.choice(
        therapy_experience_options, size=n, p=therapy_experience_probs
    )

    # Gender distribution
    gender_options = ["Male", "Female", "Other"]
    gender_probs = [0.48, 0.50, 0.02]  # Approximate global gender distribution
    genders = np.random.choice(gender_options, size=n, p=gender_probs)

    # Relationship status distribution
    relationship_status_options = ["Single", "In a relationship", "Married"]
    relationship_status_probs = [
        0.4,
        0.35,
        0.25,
    ]  # 40% Single, 35% In a relationship, 25% Married
    relationship_status = np.random.choice(
        relationship_status_options, size=n, p=relationship_status_probs
    )

    # Secure scores: Normal distribution around 6 with std dev of 2, clipped between 0 and 10
    secure_scores = np.clip(np.random.normal(loc=6, scale=2, size=n), 0, 10)

    # Initialize avoidant and anxious scores
    avoidant_scores = np.zeros(n)
    anxious_scores = np.zeros(n)

    # Generate avoidant and anxious scores based on gender
    for i in range(n):
        if genders[i] == "Male":
            # Men are more likely to be avoidant when not secure
            avoidant_mean = 6
            anxious_mean = 4
        elif genders[i] == "Female":
            # Women are more likely to be anxious when not secure
            avoidant_mean = 4
            anxious_mean = 6
        else:
            # For 'Other' gender, use a neutral mean
            avoidant_mean = 5
            anxious_mean = 5

        # Adjust means based on secure score: Lower secure scores amplify the effect
        if secure_scores[i] < 5:
            avoidant_mean += (5 - secure_scores[i]) * (
                0.5 if genders[i] == "Male" else -0.5
            )
            anxious_mean += (5 - secure_scores[i]) * (
                0.5 if genders[i] == "Female" else -0.5
            )

        # Generate scores with a standard deviation of 2, clipped between 0 and 10
        avoidant_scores[i] = np.clip(
            np.random.normal(loc=avoidant_mean, scale=2), 0, 10
        )
        anxious_scores[i] = np.clip(np.random.normal(loc=anxious_mean, scale=2), 0, 10)

    # Create the DataFrame
    df = pd.DataFrame(
        {
            "age": ages,
            "therapy_experience": therapy_experience,
            "gender": genders,
            "relationship_status": relationship_status,
            "avoidant_score": avoidant_scores.round(1),
            "secure_score": secure_scores.round(1),
            "anxious_score": anxious_scores.round(1),
        }
    )

def upload_objects_to_db(objects: list[Base]):
    with Session(engine) as session:
        session.add_all(objects)
        session.commit()
    
        