import dash_bootstrap_components as dbc
from dash import dcc

Description = dbc.Container(
    dcc.Markdown("""
    #### Welcome to the attachment style test!
    Please evaluate how much you can relate to the following statements on the scale from 0 to 10.\n
    Test Your Partner page offers more behaviour-based questions with examples that you can answer with regard to someone you know (as well as yourself).
    """),
    style={"width": "80%"},
    className="mb-4 text-center"
)
