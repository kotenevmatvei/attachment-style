import dash_bootstrap_components as dbc
from dash import dcc

QuestionCardPartner = dbc.Row(
    dbc.Col(
        dbc.Card(
            children=[
                dbc.CardHeader(
                    [
                        dbc.Button(id="left-button-partner", className="bi bi-arrow-left-circle d-flex align-items-center"),
                        dcc.Markdown("##### Question 1/42", id="question-count-text-partner", className="mx-2 px-3 pt-1 border border-3 rounded"),
                        dbc.Button(id="right-button-partner", className="bi bi-arrow-right-circle d-flex align-items-center"),
                    ],
                    className="d-flex align-items-center justify-content-center",
                    style={"height": "3.5rem"}
                ),
                dbc.CardBody(
                    dcc.Markdown("Text of the question", id="question-text-partner")
                ),
                dbc.CardFooter(
                    dbc.Container(
                        dbc.ButtonGroup(
                            [
                                dbc.Button("Strongly Disagree", id="strongly-disagree-btn-partner", color="danger"),
                                dbc.Button("Disagree", id="disagree-btn-partner", color="warning"),
                                dbc.Button("Neutral", id="neutral-btn-partner", color="secondary"),
                                dbc.Button("Agree", id="agree-btn-partner", color="info"),
                                dbc.Button("Strongly Agree", id="strongly-agree-btn-partner", color="success"),
                            ],
                            className="d-flex justify-content-center",
                        )
                    )
                ),
            ],
            style={"width": "45rem"},
            # className="text-center"
        ),
        className="mb-4 d-flex justify-content-center"
    )
)

