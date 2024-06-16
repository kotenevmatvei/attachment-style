from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
# import dash_mantine_components as dmc


from navbar import Navbar
from description import Description
from question_card import QuestionCard

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP])

app.layout = html.Div([
    Navbar,
    Description,
    QuestionCard,
    html.Div(dbc.Button("Submit"), className="text-center")
])

if __name__ == "__main__":
    app.run_server(debug=True)
