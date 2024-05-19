import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Attachment Style Test"), className="text-center mb-4")),
    dbc.Row(dbc.Col(dbc.Button("Start", id="start-button", color="primary", className="mb-4"), width={"size": 6, "offset": 3}, className="text-center")),
    dbc.Row(dbc.Col(dbc.Collapse(html.Div("Question 3/14", className="mb-2 text-center"), id="question", is_open=False))),
    dbc.Row(dbc.Col(dbc.Collapse(html.Div("Text of the question", className="mb-2 text-center"), id="question-text", is_open=False))),
    dbc.Row(dbc.Col(dbc.Collapse(dcc.Input(type="number", value=7, className="mb-4 text-center"), id="answer-input", is_open=False), width={"size": 4, "offset": 4})),
    dbc.Row(dbc.Col(dbc.Collapse(html.Div("Result", className="mb-2 text-center"), id="result", is_open=False)))
], fluid=True)

# Callback to toggle the collapse when Start button is clicked
@app.callback(
    [Output("question", "is_open"),
     Output("question-text", "is_open"),
     Output("answer-input", "is_open"),
     Output("result", "is_open")],
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
                True if not is_open_result else is_open_result)
    return is_open_question, is_open_question_text, is_open_answer_input, is_open_result

if __name__ == '__main__':
    app.run_server(debug=True)
