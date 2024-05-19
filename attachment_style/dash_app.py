import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Attachment Style Test"), className="text-center mb-4")),
    dbc.Row(dbc.Col(dbc.Button("Start", color="primary", className="mb-4"), className="text-center")),
    dbc.Row(dbc.Col(html.Div("Question 3/14", className="mb-2 text-center"))),
    dbc.Row(dbc.Col(html.Div("Text of the question", className="mb-2 text-center"))),
    dbc.Row(dbc.Col(dcc.Input(type="number", value=7, className="mb-4 text-center"))),
    dbc.Row(dbc.Col(html.Div("Result", className="mb-2 text-center"))),
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
