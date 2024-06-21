from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

from attachment_style.components.navbar import Navbar
from attachment_style.components.description import Description
from attachment_style.components.question_card import QuestionCard
from attachment_style.components.dashboard import Dashboard

from utils.utils import read_questions

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP])

app.layout = html.Div([
    Navbar,
    Description,
    QuestionCard,
    html.Div(dbc.Button("Submit Test"), className="mb-4 text-center border"),
    Dashboard,
    html.Div(dbc.Button("Download Report", id="submit-button"), className="text-center border"),
    # storage
    dcc.Store(id="questions-storage", data=read_questions(), storage_type="session"),
    dcc.Store(id="question-count-storage", data=0),
    dcc.Store(id="answers-storage", data={}),
    dcc.Store(id="last-question-visited-flag")
])

@app.callback(
    [
        Output("question-count-storage", "data"),
        Output("question-count-text", "children"),
        Output("question-text", "children"),
        Output("answers-storage", "data")
    ],
    [
        Input("right-button", "n_clicks")
    ],
    [
        State("question-count-storage", "data"),
        State("questions-storage", "data"),
        State("answers-storage", "data"),
        State("slider", "value")
    ]
)
def update_question(r_clicks, question_count, questions, answers, slider_value):
    n = len(questions)
    # first question / inital state
    if r_clicks is None:
        return (
            1,
            f"Question {1}/{n}",
            questions[0][0],
            answers
        )
    # questions between first and last
    elif question_count < n:
        answers[question_count-1] = slider_value
        print(question_count-1, answers[question_count-1])
        question_count += 1
        return (
            question_count,
            f"Question {question_count}/{n}",
            questions[question_count-1][0],
            answers
        )
    # last question
    else:
        answers[question_count-1] = slider_value
        print(question_count - 1, answers[question_count - 1])
        return (
            question_count,
            f"Question {n}/{n}",
            questions[n-1][0],
            answers
        )

if __name__ == "__main__":
    app.run_server(debug=True)
