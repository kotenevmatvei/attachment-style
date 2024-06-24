import dash_bootstrap_components as dbc
from dash import dcc

QuestionCard = dbc.Row(
    dbc.Col(
        dbc.Card(
            children=[
                dbc.CardHeader(
                    [
                        dbc.Button(id="left-button", className="bi bi-arrow-left-circle d-flex align-items-center"),
                        dcc.Markdown("##### Question 1/42", id="question-count-text", className="mx-2 px-3 pt-1 border border-3 rounded"),
                        dbc.Button(id="right-button", className="bi bi-arrow-right-circle d-flex align-items-center"),
                    ],
                    className="d-flex align-items-center justify-content-center",
                    style={"height": "3.5rem"}
                ),
                dbc.CardBody(
                    dcc.Markdown("Text of the question", id="question-text")
                ),
                dbc.CardFooter(
                    dbc.Container(
                        dcc.Slider(
                            id="slider",
                            min=0,
                            max=10,
                            step=.1,
                            value=0,
                            marks=None,
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True,
                            }
                        ),
                        style={"width": "40rem"}
                    )
                ),
            ],
            style={"width": "45rem"},
            className="border text-center"
        ),
        className="mb-4 d-flex justify-content-center"
    )
)

