from dash import Dash, html, dcc, Input, Output
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
    dcc.Store(id="questions", data=read_questions(), storage_type="session"),
    dcc.Store(id="answers")
])

@app.callback(
    Output("question-text", "children"),
    Input("questions", "data")
)
def set_question(questions):
    print(questions)
    return questions[0][0]


if __name__ == "__main__":
    app.run_server(debug=True)
