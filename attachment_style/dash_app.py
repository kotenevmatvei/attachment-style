import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State

from attachment_style_test import read_questions_file, check_same_length

# read question files
anxious_questions: list[tuple[str, str]] = read_questions_file("anxious_questions.txt", "anxious")
secure_questions: list[tuple[str, str]] = read_questions_file("secure_questions.txt", "secure")
avoidant_questions: list[tuple[str, str]] = read_questions_file("avoidant_questions.txt", "avoidant")

# check that there is the same number of questions
check_same_length(
    anxious_questions=anxious_questions,
    secure_questions=secure_questions,
    avoidant_questions=avoidant_questions
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
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Attachment Style Test"), className="text-center mb-4")),
    dbc.Row(dbc.Col(dbc.Button("Start", id="start-button", color="primary", className="mb-4"), width={"size": 6, "offset": 3}, className="text-center")),
    dbc.Row(dbc.Col(dbc.Collapse(html.Div(f"Question {question_count}/14", className="mb-2"), id="question", is_open=False), className="text-center")),
    dbc.Row(dbc.Col(dbc.Collapse(html.Div("Text of the question", className="mb-2 text-center"), id="question-text", is_open=False))),
    dbc.Row(dbc.Col(dbc.Collapse(html.Div(dcc.Input(id="answer-input-field", type="number", value=7, className="short-input mb-4"), className="text-center"), id="answer-input", is_open=False), width={"size": 4, "offset": 4})),
    dbc.Row(dbc.Col(dbc.Collapse(html.Div("Result", className="mb-2 text-center"), id="result", is_open=False)))
], fluid=True)

@app.callback(
    [Output("question", "is_open"),
     Output("question-text", "is_open"),
     Output("answer-input", "is_open"),
     Output("result", "is_open"),
     Output("start-button", "children")],  # Add this line
    [Input("start-button", "n_clicks")],
    [State("question", "is_open"),
     State("question-text", "is_open"),
     State("answer-input", "is_open"),
     State("result", "is_open")]
)
def toggle_collapse(n_clicks, is_open_question, is_open_question_text, is_open_answer_input, is_open_result):
    if n_clicks:
        return (True if not is_open_question else is_open_question,
                True if not is_open_question_text else is_open_question_text,
                True if not is_open_answer_input else is_open_answer_input,
                True if not is_open_result else is_open_result,
                "Start Again" if n_clicks >= 1 else "Start")  # Add this line
    return is_open_question, is_open_question_text, is_open_answer_input, is_open_result, "Start"  # Add "Start"

@app.callback(
    Output("question", "children"),
    [Input("answer-input-field", "n_submit")]
)
def update_question(n_submit):
    global question_count
    if n_submit is not None:
        question_count += 1
    return f"Question {question_count}/14"

if __name__ == '__main__':
    app.run_server(debug=True)
