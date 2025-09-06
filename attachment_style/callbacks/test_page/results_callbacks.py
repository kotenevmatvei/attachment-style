from dash import callback, Output, Input, State, no_update
import dash_mantine_components as dmc
from utils.utils import build_ecr_r_chart

dmc.add_figure_templates()


# update the score cards on top
@callback(
    [
        Output("anxious-score-percent-text", "children"),
        Output("avoidant-score-percent-text", "children"),
        Output("secure-score-percent-text", "children"),
    ],
    Input("result-scores-store", "data"),
    prevent_initial_callback=True,
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


@callback(
    Output("results-chart", "figure"),
    [
        Input("result-scores-store", "data"),
        Input("mantine-provider", "forceColorScheme"),
    ],
    prevent_inital_callback=True,
)
def update_results_chart(scores, theme):
    anxious_score = scores["anxious_score"]
    avoidant_score = scores["avoidant_score"]
    secure_score = scores["secure_score"]
    figure = build_ecr_r_chart(anxious_score, avoidant_score, secure_score)
    if theme == "dark":
        figure.update_layout(template="mantine_dark")
    else:
        figure.update_layout(template="mantine_light")

    return figure


