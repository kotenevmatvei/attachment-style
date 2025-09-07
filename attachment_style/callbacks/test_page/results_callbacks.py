import logging

import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash import callback, Output, Input, State, dcc, clientside_callback

from utils.generate_pdf import generate_report
from utils.utils import build_ecr_r_chart, revert_scores_for_reverted_questions

logger = logging.getLogger(__name__)

dmc.add_figure_templates()


# score cards on top
@callback(
    [
        Output("anxious-score-percent-text", "children"),
        Output("avoidant-score-percent-text", "children"),
        Output("secure-score-percent-text", "children"),
    ],
    Input("result-scores-store", "data"),
    prevent_initial_call=True,
)
def update_score_cards(scores):
    # convert to relative percentage
    total_score = scores["anxious_score"] + scores["avoidant_score"] + scores["secure_score"]
    print("total score: ", total_score)
    anxious_percent = round(((scores["anxious_score"] / total_score) * 100), 1)
    avoidant_percent = round(((scores["avoidant_score"] / total_score) * 100), 1)
    secure_percent = round(((scores["secure_score"] / total_score) * 100), 1)
    return (
        f"{anxious_percent}%",
        f"{avoidant_percent}%",
        f"{secure_percent}%",
    )


# ecr-r chart
@callback(
    [
        Output("results-chart", "figure"),
        Output("figure-store", "data"),
    ],
    [
        Input("result-scores-store", "data"),
        Input("mantine-provider", "forceColorScheme"),
    ],
    State("subject-store", "data"),
    prevent_initial_call=True,
)
def update_results_chart(scores, theme, subject):
    anxious_score = scores["anxious_score"]
    avoidant_score = scores["avoidant_score"]
    secure_score = scores["secure_score"]

    if subject == "you":
        figure = build_ecr_r_chart(anxious_score, avoidant_score, secure_score)
    else:
        df = pd.DataFrame({"style": ["Anxious Score", "Avoidant Score", "Secure Score"],
                           "scores": [anxious_score, avoidant_score, secure_score]})
        figure = px.bar(df, x="style", y="scores", color="style",
                        labels={"scores": "Your Score", "style": "Attachment Style"})
        figure.update_layout(showlegend=False)

    if theme == "dark":
        figure.update_layout(template="mantine_dark")
    else:
        figure.update_layout(template="mantine_light")

    fig_json = figure.to_json()

    return figure, fig_json


# interpretation
@callback(
    [
        Output("dominant-style-text", "children"),
        Output("result-interpretation-text", "children"),
        Output("result-interpretation-list", "children"),
    ],
    Input("result-scores-store", "data"),
    prevent_initial_call=True,
)
def update_dominant_style_text(scores):
    anxious_score = scores["anxious_score"]
    avoidant_score = scores["avoidant_score"]
    secure_score = scores["secure_score"]
    if (anxious_score >= avoidant_score) and (anxious_score >= secure_score):
        dominant_style = "Anxious"
        dominant_score = anxious_score
        interpretation_text = [
            "People with a ",
            dmc.Text("anxious attachment style", fw=600, span=True),
            " tend to crave emotional intimacy but often feel "
            "insecure and doubtful about their partner's love and commitment. They may have a negative "
            "self-view and a positive view of their partners, leading to a deep-seated fear of abandonment. "
            "This anxiety can cause them to seek constant reassurance, over-analyze their partner's behavior, and "
            "become highly dependent on the relationship for their sense of self-worth.",
        ]
        key_characteristics = [
            dmc.ListItem("Intense craving for closeness and intimacy"),
            dmc.ListItem("Persistent worry about the partner's love and the relationship's stability"),
            dmc.ListItem(
                "Tendency to be emotionally dependent on the partner"
            ),
            dmc.ListItem("High sensitivity to a partner's moods and actions"),
            dmc.ListItem(
                "Fear of being alone or rejected"
            ),
        ]
    if (secure_score >= avoidant_score) and (secure_score >= anxious_score):
        dominant_style = "Secure"
        dominant_score = secure_score
        interpretation_text = [
            "People with a ",
            dmc.Text("secure attachment style", fw=600, span=True),
            " typically feel comfortable with intimacy and are usually warm and loving. They have "
            "a positive view of themselves and their partners. They communicate effectively, are "
            "comfortable depending on others and having others depend on them, and don't worry about "
            "being alone or being accepted.",
        ]

        key_characteristics = [
            dmc.ListItem("Comfortable with emotional intimacy"),
            dmc.ListItem("Effective communication skills"),
            dmc.ListItem(
                "Balanced need for independence and closeness"
            ),
            dmc.ListItem("Positive self-image and view of others"),
            dmc.ListItem(
                "Resilient in handling relationship conflicts"
            ),
        ]
    if (avoidant_score >= secure_score) and (avoidant_score >= anxious_score):
        dominant_style = "Avoidant"
        dominant_score = avoidant_score
        interpretation_text = [
            "People with a ",
            dmc.Text("avoidant attachment style", fw=600, span=True),
            " are often highly independent and self-sufficient, preferring to handle problems on their own. "
            "They tend to be uncomfortable with emotional closeness and may suppress their feelings to avoid intimacy. "
            "While they may have a positive self-image, they can be dismissive of others' needs for closeness and may "
            "view partners as overly demanding. They prioritize their freedom and may distance themselves when they feel "
            "a partner is getting too close..",
        ]
        key_characteristics = [
            dmc.ListItem("Strong emphasis on independence and self-reliance"),
            dmc.ListItem("Discomfort with emotional intimacy and sharing feelings"),
            dmc.ListItem(
                "Tendency to create distance in relationships"
            ),
            dmc.ListItem("Avoidance of dependency on others"),
            dmc.ListItem(
                "Suppression of emotional expression"
            ),
        ]

    dominant_style_text = dmc.Text(
        [
            "Your dominant attachment style is ",
            dmc.Text(
                dominant_style,
                fw=700,
                span=True,
                c="#339AF0",
            ),
            f" with a score of {round(dominant_score, 1)} from 7.",
        ]
    ),

    return dominant_style_text, interpretation_text, key_characteristics


# download picture
@callback(
    Output("dummy-div-pic-download", "style"),
    Input("figure-store", "data"),
    prevent_initial_call=True,
)
def download_plot_picture(fig_json):
    fig = pio.from_json(fig_json)

    logger.info("Saving the image...")
    fig.write_image(
        "tmp/figure_you.png", width=700, height=500
    )
    logger.info("Image saved")

    return {}


# download pdf report
@callback(
    [
        Output("download-report", "data"),
        Output("download-report-button", "loading", allow_duplicate=True),
    ],
    Input("download-report-button", "n_clicks"),
    [
        State("answers-store", "data"),
        State("figure-store", "data"),
        State("result-scores-store", "data")
    ],
    prevent_initial_call=True,
)
def load_report(n_clicks, answers, fig_json, scores):
    if n_clicks:
        # determine dominant attachment style
        anxious_score = scores["anxious_score"]
        avoidant_score = scores["avoidant_score"]
        secure_score = scores["secure_score"]
        if (anxious_score >= avoidant_score) and (anxious_score >= secure_score):
            dominant_style = "anxious"
        if (avoidant_score >= secure_score) and (avoidant_score >= anxious_score):
            dominant_style = "avoidant"
        if (secure_score >= avoidant_score) and (secure_score >= anxious_score):
            dominant_style = "secure"

        fig = pio.from_json(fig_json)

        logger.info("Saving the image...")
        fig.write_image(
            "tmp/figure.png", width=700, height=500
        )
        logger.info("Image saved")
        reverted_scores = revert_scores_for_reverted_questions(answers)
        generate_report(reverted_scores, dominant_style)
        return dcc.send_file("tmp/attachment_style_report.pdf", type="pdf"), False

    return None, False


# show loading while downloading the pdf report
clientside_callback(
    """
    function updateLoadingState(n_clicks) {
        return true
    }
    """,
    Output("download-report-button", "loading"),
    Input("download-report-button", "n_clicks"),
    prevent_initial_call=True,
)


# clear the state when going back to survey or about page
@callback(
    [
        Output("current-question-count-store", "data", allow_duplicate=True),
        Output("questions-answered-count-store", "data", allow_duplicate=True),
        Output("answers-store", "data", allow_duplicate=True),
        Output("subject-store", "data", allow_duplicate=True),
        Output("result-scores-store", "data", allow_duplicate=True),
        Output("questions-len", "data", allow_duplicate=True),
        Output("figure-store", "data", allow_duplicate=True),
    ],
    [
        Input("retake-survey-button", "n_clicks"),
        Input("learn-more-button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def clear_state(retake_servey_clicks, learn_more_clicks):
    return 1, 0, {}, "you", {"anxious_score": 1, "avoidant_score": 1, "secure_score": 1}, 36, {}
