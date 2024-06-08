import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from plotly import express as px
from random import shuffle

from attachment_style.attachment_style_api import (
    read_questions_file,
    check_same_length,
    build_plotly_3d_plot,
)
from utils import combine_and_shuffle_lists


def calculate_scores(answers: list[dict[str, str]]) -> tuple[float, float, float]:
    anxious_score = [
        sum(
            [
                float(answer["score"])
                for answer in answers
                if answer["attachment_style"] == "anxious"
            ]
        )
    ]
    secure_score = [
        sum(
            [
                float(answer["score"])
                for answer in answers
                if answer["attachment_style"] == "secure"
            ]
        )
    ]
    avoidant_score = [
        sum(
            [
                float(answer["score"])
                for answer in answers
                if answer["attachment_style"] == "avoidant"
            ]
        )
    ]
    return anxious_score, secure_score, avoidant_score


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
                    id="question-count-collapse",
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
                    id="show-results-collapse",
                    is_open=False,
                    class_name="text-center",
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Collapse(
                    children=[
                        html.Div("Result", className="mb-2 text-center border"),
                        dcc.Graph(figure=px.scatter([1, 2, 3]), id="3d-figure"),
                    ],
                    id="result-collapse",
                    is_open=False,
                )
            )
        ),
        dcc.Interval(id="page-load", interval=1, max_intervals=1),
        dcc.Store(id="questions-store", data=questions),
        dcc.Store(id="question-count-store", data=1),
        dcc.Store(id="answers", data=[]),
    ],
    fluid=True,
)

# app.layout = layout

@app.callback(
    Output('questions-store', 'data'),
    (Input('page-load', 'n_intervals'),)  # Change this line
)
def shuffle_questions(n):
    shuffled_questions = questions.copy()
    shuffle(shuffled_questions)
    return shuffled_questions


# Reveal the hidden elements after the click on start
@app.callback(
    [
        Output("question-count-collapse", "is_open"),
        Output("question-text", "is_open"),
        Output("answer-input", "is_open"),
        Output("start-button", "children"),
    ],
    [Input("start-button", "n_clicks")],
    [
        State("question-count-collapse", "is_open"),
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
    Output("question-count-collapse", "children"),
    Output("question-text", "children"),
    Output("answers", "data"),
    Output("show-results-collapse", "is_open"),
    [
        Input("answer-input-field", "n_submit"),
        Input("questions-store", "data")
    ],
    [
        State("question-count-store", "data"),
        State("answer-input-field", "value"),
        State("answers", "data"),
    ],
)
def update_question(n_submit, questions, question_count_store, score, answers):
    questions = questions
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
                "score": score / 14,
            }
        )
        question_count_store += 1
        return (
            question_count_store,
            f"Question {question_count_store}/{len(questions)}",
            questions[question_count_store - 1][0],
            answers,
            False,
        )
    answers.append(
        {
            "question": questions[-1][0],
            "attachment_style": questions[-1][1],
            "score": score / 14,
        }
    )
    return (
        question_count_store,
        f"Question {len(questions)}/{len(questions)}",
        "No more questions",
        answers,
        True,
    )


@app.callback(
    [Output("result-collapse", "is_open"), Output("3d-figure", "figure")],
    Input("show-results-button", "n_clicks"),
    [State("answers", "data")],
)
def show_result(n_clicks, data):
    anxious_score, secure_score, avoidant_score = calculate_scores(data)
    fig = build_plotly_3d_plot(
        number_of_questions=len(questions),
        anxious_score=anxious_score,
        secure_score=secure_score,
        avoidant_score=avoidant_score,
    )
    print(data)
    if n_clicks == 0:
        return False, px.scatter([1, 2])
    else:
        return True, fig


if __name__ == "__main__":
    app.run_server(debug=True)
