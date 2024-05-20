import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State

from attachment_style_test import read_questions_file, check_same_length
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

# setup the lists to store the results
# Setup the lists to store the results
anxious_results: dict[str, int] = {}
secure_results: dict[str, int] = {}
avoidant_results: dict[str, int] = {}

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
                    "Start", id="start-button", n_clicks=0, color="primary", className="mb-4"
                ),
                class_name="text-center"
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
                    html.Div("Result", className="mb-2 text-center border"),
                    id="result",
                    is_open=False,
                )
            )
        ),
        dcc.Store(id="question-count-store", data=1),
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
    Output('question-count-store', 'data'),
    Output("question-count", "children"),
    Output("question-text", "children"),
    [Input("answer-input-field", "n_submit")],
    [State('question-count-store', 'data')]
)
def update_question(n_submit, question_count_store):
    if n_submit is None:
        return question_count_store, "Question 1/1", questions[question_count_store - 1][0]
    elif n_submit is not None and question_count_store < 42:
        question_count_store += 1
        return question_count_store, f"Question {question_count_store}/42", questions[question_count_store - 1][0]
    return question_count_store, "Question 42/42", "No more questions"
    
if __name__ == "__main__":
    app.run_server(debug=True)
