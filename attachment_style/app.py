from dash import Dash, html, dcc, Input, Output, State, ctx
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
    html.Div(id="log"),
    html.Div(dbc.Button("Submit Test"), className="mb-4 text-center border"),
    Dashboard,
    html.Div(dbc.Button("Download Report", id="submit-button"), className="text-center border"),
    # storage
    dcc.Store(id="questions-storage", data=read_questions(), storage_type="session"),
    dcc.Store(id="question-count-storage", data=0),
    dcc.Store(id="answers-storage", data={}),
    dcc.Store(id="lb-visited-last-storage")
])


@app.callback(
    Output("log", "children"),
    Input("answers-storage", "data"),
    Input("lb-visited-last-storage", "data")
)
def update_question_count_ref(answers, lb_last_visited):
    return f"log: last_visited: {lb_last_visited}, {answers}"


@app.callback(
    [
        Output("question-count-storage", "data"),
        Output("question-count-text", "children"),
        Output("question-text", "children"),
        Output("answers-storage", "data"),
        Output("slider", "value"),
        Output("lb-visited-last-storage", "data")
    ],
    [
        Input("right-button", "n_clicks"),
        Input("left-button", "n_clicks"),
        Input("slider", "value")
    ],
    [
        State("question-count-storage", "data"),
        State("questions-storage", "data"),
        State("answers-storage", "data"),
        State("lb-visited-last-storage", "data")
    ]
)
def update_question(
        r_clicks: int,
        l_clicks: int,
        slider_value: float,
        question_count: int,
        questions: list[tuple[str, str]],
        answers: dict[str, tuple[str, float]],
        lb_visited_last: bool
):
    n: int = len(questions)
    id_triggered = ctx.triggered_id
    match id_triggered:
        case "right-button":
            # questions between first and last
            if question_count < n:
                answers[f"{question_count-1}"] = (questions[question_count-1][1], slider_value)
                question_count += 1
                if f"{question_count}" in answers.keys():
                    return (
                        question_count,
                        f"Question {question_count}/{n}",
                        questions[question_count-1][0],
                        answers,
                        answers[f"{question_count-1}"][1],
                        False
                    )
                else:
                    return (
                        question_count,
                        f"Question {question_count}/{n}",
                        questions[question_count-1][0],
                        answers,
                        0,
                        False
                    )
            # last question
            else:
                answers[f"{question_count-1}"] = (questions[question_count-1][1], slider_value)
                return (
                    question_count,
                    f"Question {n}/{n}",
                    questions[n-1][0],
                    answers,
                    answers[f"{question_count-1}"][1],
                    False
                )

        case "slider":
            # questions between first and last
            if question_count < n:
                answers[f"{question_count - 1}"] = (questions[question_count - 1][1], slider_value)
                if not lb_visited_last:
                    question_count += 1
                    if f"{question_count}" in answers.keys():
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            answers[f"{question_count}"][1],
                            False
                        )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            0,
                            False
                        )
                else:
                    return (
                        question_count,
                        f"Question {question_count}/{n}",
                        questions[question_count - 1][0],
                        answers,
                        answers[f"{question_count-1}"][1],
                        False
                    )
            # last question
            else:
                answers[f"{question_count - 1}"] = (questions[question_count - 1][1], slider_value)
                return (
                    question_count,
                    f"Question {n}/{n}",
                    questions[n - 1][0],
                    answers,
                    answers[f"{question_count - 1}"][1],
                    False
                )

        case "left-button":
            if question_count == 1:
                answers["0"] = (questions[0][1], slider_value)
                return (
                    1,
                    f"Question 1/{n}",
                    questions[0][0],
                    answers,
                    answers["0"][1],
                    True
                )
            else:
                answers[f"{question_count-1}"] = (questions[question_count-1][1], slider_value)
                return (
                    question_count-1,
                    f"Question {question_count-1}/{n}",
                    questions[question_count-2][0],
                    answers,
                    answers[f"{question_count - 2}"][1],
                    True
                )

    # first question / initial state
    return (
        1,
        f"Question {1}/{n}",
        questions[0][0],
        answers,
        0,
        False
    )


if __name__ == "__main__":
    app.run_server(debug=True)
