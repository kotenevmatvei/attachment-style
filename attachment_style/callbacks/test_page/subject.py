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
        Output("question-content-flex", "justify")
    ],
    Input("subject-store", "data"),
)
def update_current_subject(subject):
    if subject == "others":
        questions = read_questions("others")
        return questions, 33, {"textAlign": "left"}, "230px", "start"

    questions = read_questions("you")
    return questions, 36, {"textAlign": "center"}, "100px", "center"
