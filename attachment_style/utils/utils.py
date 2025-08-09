import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import pandas as pd
import os
import logging
import codecs
from sqlalchemy.engine import result
from sqlalchemy.orm import Session
from sqlalchemy import literal_column, select, union_all
from datetime import datetime as dt
from datetime import timedelta
from models import (
    Base,
    AssessYourself,
    AssessOthers,
)  # import works while utils imported in app.py
from sqlalchemy import create_engine, select
# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

# production url
# url = str(os.getenv("DB_URL_DEBUG"))

try:
    DB_URL = os.environ['DB_URL']
except KeyError:
    raise RuntimeError("DB_URL environment variable not set.")

engine = create_engine(url=DB_URL)


def read_questions_file(
    questions_file_path: str, attachment_style: str
) -> list[tuple[str, str]]:
    """Read the txt file with questions and add them to the corresponding list."""
    questions_list: list[tuple[str, str]] = []
    with open(questions_file_path, "r") as file:
        for line in file:
            decoded_line = codecs.decode(line.strip(), "unicode_escape")
            line_with_reverse_score_accounted = decoded_line.replace(" /r/", "  ")
            questions_list.append((line_with_reverse_score_accounted, attachment_style))

    return questions_list


def revert_questions(
    answers: dict[str, tuple[str, float, str]],
) -> dict[str, tuple[str, float, str]]:
    # revert the questions when needed (only relevant for ecr-r)
    if len(answers) == 36:
        for key, value in answers.items():
            if value[2].endswith("  "):
                reverted_value = (value[0], abs(8 - value[1]), value[2])
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
        x_and_y_coord = (anxious_score + avoidant_score) / 2
        sign = np.sign(x_and_y_coord)
        secure_score = np.sqrt(2 * (x_and_y_coord) ** 2) * sign

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
    fig.update_layout(margin={"t": 40})

    return fig


def build_ecr_r_chart(anxious_score: float, secure_score: float, avoidant_score: float):
    # Set default renderer to browser
    # pio.renderers.default = "browser"

    # --- Define the 1-7 scale parameters ---
    scale_min = 1
    scale_max = 7
    scale_mid = (scale_min + scale_max) / 2  # This will be 4

    # --- USER INPUT: Define your extra point's coordinates here (on the 1-7 scale) ---
    # Anxiety: 1 (low) to 7 (high)
    # Avoidance: 1 (low, top of plot) to 7 (high, bottom of plot)
    # Ensure the point is not directly on the main axes (x=4, y=4) or the y=x diagonal
    # for clear projection lines.
    extra_point_coords = {
        "anxiety": anxious_score,
        "avoidance": avoidant_score,
        "text": f"({round(anxious_score, 1)}, {round(avoidant_score, 1)})",
    }
    # --- END USER INPUT ---

    xp = extra_point_coords["anxiety"]
    yp = extra_point_coords["avoidance"]

    # Create the figure
    fig = go.Figure()

    # Define plot range to give some space around the 1-7 scale
    plot_range_min = 0
    plot_range_max = 8

    # 1. Draw Main Conceptual Axes (Anxiety and Avoidance)
    # Horizontal Anxiety Axis (conceptually at y=scale_mid)
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_mid,
        x1=scale_max,
        y1=scale_mid,
        line=dict(color="black", width=2),
    )

    # Vertical Avoidance Axis (conceptually at x=scale_mid)
    fig.add_shape(
        type="line",
        x0=scale_mid,
        y0=scale_min,
        x1=scale_mid,
        y1=scale_max,
        line=dict(color="black", width=2),
    )

    # 2. Draw Diagonal Axes
    # Secure (1,1) to Fearful-Avoidant (7,7)
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_min,
        x1=scale_max,
        y1=scale_max,
        line=dict(color="darkgrey", width=1, dash="dash"),
    )
    # Dismissive (1,7) to Preoccupied (7,1)
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_max,
        x1=scale_max,
        y1=scale_min,
        line=dict(color="darkgrey", width=1, dash="dash"),
    )

    # 3. Add Ticks (dots) and Labels for Axes
    tick_values = list(range(scale_min, scale_max + 1))
    tick_marker_style = dict(color="black", size=6)
    tick_label_font_style = dict(size=10, color="black")

    # Anxiety Axis Ticks (on the line y=scale_mid)
    fig.add_trace(
        go.Scatter(
            x=tick_values,
            y=[scale_mid] * len(tick_values),
            mode="markers+text",
            marker=tick_marker_style,
            text=["1", "2", "3", "", "5", "6", "7"],
            textposition="bottom center",
            textfont=tick_label_font_style,
            hoverinfo="none",
        )
    )

    # Avoidance Axis Ticks (on the line x=scale_mid)
    fig.add_trace(
        go.Scatter(
            x=[scale_mid] * len(tick_values),
            y=tick_values,
            mode="markers+text",
            marker=tick_marker_style,
            text=["1", "2", "3", "", "5", "6", "7"],
            textposition="middle right",  # Adjusted for y-axis ticks
            textfont=tick_label_font_style,
            hoverinfo="none",
        )
    )

    # Secure - Fearful-Avoidant Diagonal Ticks (on the line y=x)
    fig.add_trace(
        go.Scatter(
            x=tick_values,
            y=tick_values,
            mode="markers+text",
            marker=tick_marker_style,
            text=[str(val) for val in tick_values[::-1]],
            textposition="top right",  # Adjust as needed for diagonal
            textfont=tick_label_font_style,
            hoverinfo="none",
        )
    )

    # 4. Add Axis Labels (Low/High)
    axis_label_font_style = dict(size=12)
    # Anxiety Axis Labels
    fig.add_annotation(
        x=scale_min - 0.5,
        y=scale_mid - 0.25,
        text="low anxiety",
        showarrow=False,
        xanchor="center",
        font=axis_label_font_style,
    )
    fig.add_annotation(
        x=scale_max + 0.5,
        y=scale_mid - 0.25,
        text="high anxiety",
        showarrow=False,
        xanchor="center",
        font=axis_label_font_style,
    )
    # Avoidance Axis Labels
    fig.add_annotation(
        x=scale_mid + 0.5,
        y=scale_min,
        text="low avoidance",
        showarrow=False,
        yanchor="middle",
        xanchor="left",
        textangle=0,
        font=axis_label_font_style,
    )
    fig.add_annotation(
        x=scale_mid + 0.5,
        y=scale_max,
        text="high avoidance",
        showarrow=False,
        yanchor="middle",
        xanchor="left",
        textangle=0,
        font=axis_label_font_style,
    )
    # Secure-Fearful-Avoidant Axis Label (Optional - can get crowded)
    # fig.add_annotation(x=scale_max, y=scale_max + 0.3, text="Secure-Fearful", showarrow=False, font=dict(size=10))
    # 5. Add Attachment Style Labels in Quadrants
    style_label_font_style = dict(size=14, color="dimgray")
    fig.add_annotation(
        x=scale_min,
        y=scale_min + 0.4,
        text="<i>secure</i>",
        showarrow=False,
        xanchor="right",
        font=style_label_font_style,
    )
    fig.add_annotation(
        x=scale_max,
        y=scale_min + 0.4,
        text="<i>preoccupied</i>",
        showarrow=False,
        xanchor="left",
        font=style_label_font_style,
    )
    fig.add_annotation(
        x=scale_min,
        y=scale_max - 0.4,
        text="<i>dismissive</i>",
        showarrow=False,
        xanchor="right",
        font=style_label_font_style,
    )
    fig.add_annotation(
        x=scale_max,
        y=scale_max - 0.4,
        text="<i>fearful-avoidant</i>",
        showarrow=False,
        xanchor="left",
        font=style_label_font_style,
    )

    # add the legend of the results
    fig.add_annotation(
        x=scale_min,
        y=scale_min - 0.8,
        text=f"Your anxious score: {round(anxious_score, 2)}, "
        f"Your avoidant score: {round(avoidant_score, 2)}",
        showarrow=False,
        yanchor="middle",
        xanchor="left",
        textangle=0,
        font={"size": 16, "color": "red", "weight": "bold"},
    )

    # 6. Add the Extra Point
    fig.add_trace(
        go.Scatter(
            x=[xp],
            y=[yp],
            mode="markers",
            marker=dict(color="red", size=12, symbol="diamond"),
            text=[extra_point_coords["text"]],
            textposition="bottom left",
            hoverinfo="text",
            textfont=dict(size=12, color="red"),
        )
    )

    # 7. Add Projection Lines for the Extra Point
    projection_line_style = dict(color="rgba(255,0,0,0.5)", width=1, dash="dot")

    # Projection to Anxiety Axis (horizontal line at y=scale_mid)
    proj_anxiety_x = xp
    proj_anxiety_y = scale_mid
    fig.add_shape(
        type="line",
        x0=xp,
        y0=yp,
        x1=proj_anxiety_x,
        y1=proj_anxiety_y,
        line=projection_line_style,
    )
    fig.add_trace(
        go.Scatter(
            x=[proj_anxiety_x],
            y=[proj_anxiety_y],
            mode="markers",
            marker=dict(
                color=projection_line_style["color"], size=5, symbol="circle-open"
            ),
            hoverinfo="none",
        )
    )

    # Projection to Avoidance Axis (vertical line at x=scale_mid)
    proj_avoidance_x = scale_mid
    proj_avoidance_y = yp
    fig.add_shape(
        type="line",
        x0=xp,
        y0=yp,
        x1=proj_avoidance_x,
        y1=proj_avoidance_y,
        line=projection_line_style,
    )
    fig.add_trace(
        go.Scatter(
            x=[proj_avoidance_x],
            y=[proj_avoidance_y],
            mode="markers",
            marker=dict(
                color=projection_line_style["color"], size=5, symbol="circle-open"
            ),
            hoverinfo="none",
        )
    )

    # Projection to Secure-Fearful-Avoidant Diagonal (y=x)
    # Formula for projection point: ((xp + yp) / 2, (xp + yp) / 2)
    proj_diag_x = (xp + yp) / 2
    proj_diag_y = (xp + yp) / 2
    fig.add_shape(
        type="line",
        x0=xp,
        y0=yp,
        x1=proj_diag_x,
        y1=proj_diag_y,
        line=projection_line_style,
    )
    fig.add_trace(
        go.Scatter(
            x=[proj_diag_x],
            y=[proj_diag_y],
            mode="markers",
            marker=dict(
                color=projection_line_style["color"], size=5, symbol="circle-open"
            ),
            hoverinfo="none",
        )
    )

    # Update layout
    fig.update_layout(
        xaxis=dict(
            range=[plot_range_min, plot_range_max],
            showgrid=False,
            zeroline=False,
            showticklabels=False,  # We are drawing our own ticks/labels
            title_text="Anxiety Dimension",  # Hidden but good for context
        ),
        yaxis=dict(
            range=[plot_range_min, plot_range_max],
            showgrid=False,
            zeroline=False,
            showticklabels=False,  # We are drawing our own ticks/labels
            title_text="Avoidance Dimension",  # Hidden but good for context
            scaleanchor="x",  # Ensures aspect ratio is 1:1
            scaleratio=1,
        ),
        width=800,
        height=800,
        margin=dict(l=50, r=50, b=50, t=50),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    # Invert y-axis (low avoidance at top [y=1], high avoidance at bottom [y=7])
    fig.update_yaxes(autorange="reversed")

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


def read_questions(subject: str) -> list[tuple[str, str]]:
    questions: list[tuple[str, str]] = []
    if subject == "you":
        questions.extend(
            read_questions_file(
                questions_file_path="data/ecr-r/anxious.txt",
                attachment_style="anxious",
            )
        )
        # questions.extend(
        #     read_questions_file(
        #         questions_file_path="data/ecr-r/secure.txt",
        #         attachment_style="secure",
        #     )
        # )
        questions.extend(
            read_questions_file(
                questions_file_path="data/ecr-r/avoidant.txt",
                attachment_style="avoidant",
            )
        )
    else:
        questions.extend(
            read_questions_file(
                questions_file_path="data/partner/anxious.txt",
                attachment_style="anxious",
            )
        )
        questions.extend(
            read_questions_file(
                questions_file_path="data/partner/secure.txt", attachment_style="secure"
            )
        )
        questions.extend(
            read_questions_file(
                questions_file_path="data/partner/avoidant.txt",
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
    fig.update_traces(textfont={"size": 20})


def upload_to_db(
    answers: dict[str, tuple[str, float, str]],
    personal_answers: dict[str, str],
    test: bool = True,
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

    if len(values) == 36:
        result_object = AssessYourself(
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
            anxious_q15=values[14],
            anxious_q16=values[15],
            anxious_q17=values[16],
            anxious_q18=values[17],
            avoidant_q1=values[0],
            avoidant_q2=values[1],
            avoidant_q3=values[2],
            avoidant_q4=values[3],
            avoidant_q5=values[4],
            avoidant_q6=values[5],
            avoidant_q7=values[6],
            avoidant_q8=values[7],
            avoidant_q9=values[8],
            avoidant_q10=values[9],
            avoidant_q11=values[10],
            avoidant_q12=values[11],
            avoidant_q13=values[12],
            avoidant_q14=values[13],
            avoidant_q15=values[14],
            avoidant_q16=values[15],
            avoidant_q17=values[16],
            avoidant_q18=values[17],
        )
    elif len(values) == 33:
        result_object = AssessOthers(
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
        assess_yourself = (
            session.query(AssessYourself).filter(AssessYourself.test == test).all()
        )
        assess_others = (
            session.query(AssessOthers).filter(AssessOthers.test == test).all()
        )
        # Convert query results to DataFrame
        assess_yourself_df = pd.DataFrame(
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
                for t in assess_yourself
            ]
        )
        assess_others_df = pd.DataFrame(
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
                for t in assess_others
            ]
        )

        session.commit()
        return assess_yourself_df, assess_others_df


def retrieve_scores_from_db():
    stmt_you = select(
        literal_column("'AssessYourself'").label("source"),
        AssessYourself.age,
        AssessYourself.gender,
        AssessYourself.relationship_status,
        AssessYourself.therapy_experience,
        AssessYourself.anxious_score,
        AssessYourself.avoidant_score,
        AssessYourself.secure_score,
        AssessYourself.test,
    )
    stmt_others = select(
        literal_column("'AssessOthers'").label("source"),
        AssessOthers.age,
        AssessOthers.gender,
        AssessOthers.relationship_status,
        AssessOthers.therapy_experience,
        AssessOthers.anxious_score,
        AssessOthers.avoidant_score,
        AssessOthers.secure_score,
        AssessOthers.test,
    )
    query = union_all(stmt_you, stmt_others)

    with Session(engine) as session:
        results = session.execute(query).all()
        if not results:
            raise ValueError("No entries in the database...")

        # this is a list of dictionaries each representing one db entry:
        results_records_dict = [row._asdict() for row in results]

        keys = results_records_dict[0].keys()
        # this is one dictionary with column names as keys - what we need for plots
        results_long_dict = {
            key: [row[key] for row in results_records_dict] for key in keys
        }

        if not results_long_dict:
            logger.error("No data was retrieved from the database")
        
        for score in ["secure_score", "avoidant_score", "anxious_score"]:
            if None in results_long_dict[score]:
                logger.critical(f"None values in column {score}!!!")

        logger.info("Successfully retrieved the data from the database")
        return results_long_dict

    # the two below are done by the database now

    # def derive_secure_score(anxious_scores, avoidant_scores):
    #     # we need to first invert the scores to get the x- and y coordinates due to the
    #     # funky scale of the ecr-r chart (two origins)
    #     secure_score = []
    #     for x, y in zip(anxious_scores, avoidant_scores):
    #         diff_x = 4 - x
    #         diff_y = 4 - y
    #         diff = (diff_x + diff_y) / 2
    #         score = 4 + diff
    #         secure_score.append(score)
    #
    #     return secure_score

    # def aggregate_scores(assess_yourself_df, assess_others_df):
    #     # todo maybe unnecessary to keep the entire dataframes? - just return the arrays, no?
    #
    #     you_anxious_score = assess_yourself_df.filter(like="anxious").sum(axis=1) / 18
    #     you_avoidant_score = assess_yourself_df.filter(like="avoidant").sum(axis=1) / 18
    #     assess_yourself_df["anxious_score"] = you_anxious_score
    #     assess_yourself_df["avoidant_score"] = you_avoidant_score
    #
    #     you_secure_score = derive_secure_score(you_anxious_score, you_avoidant_score)
    #
    #     assess_yourself_df["secure_score"] = you_secure_score
    #
    #     assess_others_df["anxious_score"] = (
    #         assess_others_df.filter(like="anxious").sum(axis=1) / 11
    #     )
    #     assess_others_df["secure_score"] = (
    #         assess_others_df.filter(like="secure").sum(axis=1) / 11
    #     )
    #     assess_others_df["avoidant_score"] = (
    #         assess_others_df.filter(like="avoidant").sum(axis=1) / 11
    #     )
    #
    #     retrieve_scores_from_db()
    #
    #     return assess_yourself_df, assess_others_df


def upload_objects_to_db(objects: list[Base]):
    with Session(engine) as session:
        session.add_all(objects)
        session.commit()
