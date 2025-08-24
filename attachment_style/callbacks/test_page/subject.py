import dash_mantine_components as dmc
from dash import callback, Input, Output, ctx

from utils.utils import read_questions


@callback(
    Output("subject-store", "data"),
    [
        Input("assess-yourself-button", "n_clicks"),
        Input("assess-others-button", "n_clicks"),
    ]
)
def update_subject_store(assess_yourself_click, assess_others_click):
    triggered_id = ctx.triggered_id
    if triggered_id == "assess-others-button":
        return "others"
    return "you"


@callback(
    [
        Output("questions-store", "data"),
        Output("questions-len", "data"),
        Output("question-markdown", "style"),
        Output("question-paper", "h"),
        Output("question-content-flex", "justify"),
        Output("progress-bar", "children")
    ],
    Input("subject-store", "data"),
)
def update_current_subject(subject):
    # first generate the steps for the progress bar
    questions_len = 36 if subject == "you" else 33
    progress_steps = dmc.Grid(
        columns=questions_len,
        children=[
            dmc.GridCol(
                dmc.Paper(" ", h=18, id={"type": "question-indicator", "index": i}, radius="xl", shadow="xl"), span=1
            )
            for i in range(1, questions_len + 1)
        ],
        gutter=5,
        w="100%",
    )

    if subject == "others":
        questions = read_questions("others")
        return questions, 33, {"textAlign": "left"}, "230px", "start", progress_steps

    questions = read_questions("you")
    return questions, 36, {"textAlign": "center"}, "100px", "center", progress_steps

