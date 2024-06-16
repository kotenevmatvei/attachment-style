import dash_bootstrap_components as dbc
# from dash_mantine_components import ActionIcon
# from dash_iconify import DashIconify
from dash import dcc, html

QuestionCard = dbc.Row(
    dbc.Col(
        dbc.Card(
            children=[
                dbc.CardHeader(
                    [
                        dbc.Button(className="bi bi-arrow-left-circle d-flex align-items-center"),
                        dcc.Markdown("##### Question 1/42", className="mx-2 px-3 pt-1 border border-3 rounded"),
                        dbc.Button(className="bi bi-arrow-right-circle d-flex align-items-center"),
                    ],
                    className="d-flex align-items-center justify-content-center",
                    style={"height": "3.5rem"}
                ),
                dbc.CardBody(
                    dcc.Markdown("Text of the question")
                ),
                dbc.CardFooter(
                    dcc.Slider(min=0, max=10, step=.1, value=5, marks=None, tooltip={"placement": "bottom", "always_visible": False})
                )
            ],
            style={"width": "45rem"},
            className="border text-center"
        ),
        className="mb-4 d-flex justify-content-center"
    )
)

