import dash_bootstrap_components as dbc
from dash import dcc, html

question_card = dbc.Row(
    dbc.Col(
        dbc.Card(
            children=[
                dbc.CardHeader(
                    dcc.Markdown("Question 1/42"),
                    style={"height": "2.5rem"}
                ),
                dbc.CardBody(
                    html.H4("Card Header")
                ),
            ],
            style={"width": "50rem"},
            className="border text-center"
        ),
        className="mb-4 d-flex justify-content-center"
    )
)

