import dash_bootstrap_components as dbc
from dash import dcc

QuestionCardOthers = dbc.Row(
    dbc.Col(
        dbc.Card(
            children=[
                dbc.CardHeader(
                    [
                        dcc.Markdown(
                            "##### Question 1/42",
                            id="question-count-text-partner",
                            className="mx-2 px-3 pt-1 border border-3 rounded",
                        ),
                    ],
                    className="d-flex align-items-center justify-content-center",
                    style={"height": "3.5rem"},
                ),
                dbc.CardBody(
                    dcc.Markdown("Text of the question", id="question-text-partner")
                ),
                dbc.CardFooter(
                    [
                        dbc.Button(
                            id="left-button-partner",
                            className="bi bi-arrow-left-circle d-flex align-items-center",
                        ),
                        dbc.Container(
                            dcc.Slider(
                                id="slider-partner",
                                min=0,
                                max=10,
                                step=1,
                                value=0,
                                marks={
                                    0: "0",
                                    1: "1",
                                    2: "2",
                                    3: "3",
                                    4: "4",
                                    5: "5",
                                    6: "6",
                                    7: "7",
                                    8: "8",
                                    9: "9",
                                    10: "10",
                                },
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True,
                                },
                            ),
                            style={"width": "90%"},
                        ),
                        dbc.Button(
                            id="right-button-partner",
                            className="bi bi-arrow-right-circle d-flex align-items-center",
                        ),
                    ],
                    style={"display": "flex"}
                ),
            ],
            style={"width": "45rem"},
            # className="text-center"
        ),
        className="mb-4 d-flex justify-content-center",
    )
)
