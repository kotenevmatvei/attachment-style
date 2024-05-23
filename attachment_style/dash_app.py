import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from plotly import express as px

from attachment_style.attachment_style_api import (
    read_questions_file,
    check_same_length,
)
from utils import combine_and_shuffle_lists

# read question files
anxious_questions: list[tuple[str, str]] = read_questions_file(
    "anxious_questions.txt", "anxious"
)
secure_questions: list[tuple[str, str]] = read_questions_file(
    "secure_questions.txt", "secure"
)
avoidant_questions: list[tuple[str, str]] = read_questions_file(
    "avoidant_questions.txt", "avoidant"
)

# check that there is the same number of questions
check_same_length(
    anxious_questions=anxious_questions,
    secure_questions=secure_questions,
    avoidant_questions=avoidant_questions,
)

questions: list[tuple[str, str]] = combine_and_shuffle_lists(
    anxious_questions, secure_questions, avoidant_questions
)

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define a variable to store the question count
question_count = 1

# Define the layout of the app
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Attachment Style Test"), className="mb-4 text-center")
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Start",
                    id="start-button",
                    n_clicks=0,
                    color="primary",
                    className="mb-4",
                ),
                class_name="text-center",
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Collapse(
                    html.Div(f"Question {question_count}/42", className="mb-2"),
                    id="question-count",
                    is_open=False,
                ),
                className="text-center",
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Collapse(
                    html.Div("Text of the question", className="mb-2"),
                    id="question-text",
                    is_open=False,
                ),
                class_name="text-center",
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Collapse(
                    html.Div(
                        dcc.Input(
                            id="answer-input-field",
                            type="number",
                            value=7,
                            className="short-input mb-4",
                        )
                    ),
                    id="answer-input",
                    class_name="text-center",
                    is_open=False,
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Collapse(
                    dbc.Button("Show Results", n_clicks=0, id="show-results-button"),
                    id = "show-results-collapse",
                    is_open=False,
                    class_name="text-center"
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Collapse(
                    children=[
                        html.Div("Result", className="mb-2 text-center border"),
                        dcc.Graph(figure=px.scatter(x=[1, 2, 3], y=[1, 4, 9])),
                    ],
                    id="result-collapse",
                    is_open=False,
                )
            )
        ),
        dcc.Store(id="question-count-store", data=1),
        dcc.Store(id="answers", data=[]),
    ],
    fluid=True,
)


# Reveal the hidden elements after the click on start
@app.callback(
    [
        Output("question-count", "is_open"),
        Output("question-text", "is_open"),
        Output("answer-input", "is_open"),
        Output("start-button", "children"),
    ],
    [Input("start-button", "n_clicks")],
    [
        State("question-count", "is_open"),
        State("question-text", "is_open"),
        State("answer-input", "is_open"),
    ],
)
def toggle_collapse(
    n_clicks,
    is_open_question_count,
    is_open_question_text,
    is_open_answer_input,
):
    if n_clicks:
        return (
            True if not is_open_question_count else is_open_question_count,
            True if not is_open_question_text else is_open_question_text,
            True if not is_open_answer_input else is_open_answer_input,
            "Start Again" if n_clicks >= 1 else "Start",
        )
    return (
        is_open_question_count,
        is_open_question_text,
        is_open_answer_input,
        "Start",
    )


# update the question count and question text on input submit
@app.callback(
    Output("question-count-store", "data"),
    Output("question-count", "children"),
    Output("question-text", "children"),
    Output("answers", "data"),
    Output("show-results-collapse", "is_open"),
    [Input("answer-input-field", "n_submit")],
    [
        State("question-count-store", "data"),
        State("answer-input-field", "value"),
        State("answers", "data"),
    ],
)
def update_question(n_submit, question_count_store, score, answers):
    if n_submit is None:
        return (
            question_count_store,
            f"Question 1/{len(questions)}",
            questions[question_count_store - 1][0],
            answers,
            False,
        )
    elif n_submit is not None and question_count_store < len(questions):
        answers.append(
            {
                "question": questions[question_count_store - 1][0],
                "attachment_style": questions[question_count_store - 1][1],
                "score": score / 10,
            }
        )
        question_count_store += 1
        return (
            question_count_store,
            f"Question {question_count_store}/{len(questions)}",
            questions[question_count_store - 1][0],
            answers,
            False
        )
    for answer in answers:
        print(answer)
    return (
        question_count_store,
        f"Question {len(questions)}/{len(questions)}",
        "No more questions",
        answers,
        True
    )


@app.callback(
    Output("result-collapse", "is_open"),
    Input("show-results-button", "n_clicks")
)
def show_result(n_clicks):
    if n_clicks >= 1:
        return True

if __name__ == "__main__":
    app.run_server(debug=True)
