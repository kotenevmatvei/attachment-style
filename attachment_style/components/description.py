import dash_bootstrap_components as dbc
from dash import dcc

Description = dbc.Container(
    dcc.Markdown("""
    #### Welcome to the attachment style test!
    Please evaluate the following statements with regard to yourself or someone else on the scale from 1 to 10.
    """),
    className="mb-4 text-center"
)
