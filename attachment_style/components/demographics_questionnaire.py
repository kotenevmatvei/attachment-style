import dash_bootstrap_components as dbc
from dash import html

DemographicsQuestionnaire = dbc.Container(
    [
        # description
        dbc.Row(
            dbc.Col(
                html.Div(
                    """
                    Please fill out the following form to help us understand your background:
                    """,
                ),
                className="text-center mb-2",
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Age:"),
                        dbc.Input(type="number", id="age"),
                    ],
                    sm={"size": 4, "offset": 2},
                    width=12,
                ),
                dbc.Col(
                    [
                        html.Div("Relationship status:"),
                        dbc.Select(
                            id="relationship-status",
                            options=[
                                {"label": "Single", "value": "single"},
                                {"label": "In a relationship", "value": "relationship"},
                                {"label": "Married", "value": "married"},
                            ],
                        ),
                    ],
                    sm=4,
                    width=12,
                ),
            ],
            className="mb-4 mb-2-xs",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Gender:"),
                        dbc.Select(
                            id="gender",
                            options=[
                                {"label": "Male", "value": "male"},
                                {"label": "Female", "value": "female"},
                                {"label": "Other", "value": "other"},
                            ],
                        ),
                    ],
                    sm={"size": 4, "offset": 2},
                    width=12,
                ),
                dbc.Col(
                    [
                        html.Div("Previous therapy experience:"),
                        dbc.Select(
                            id="therapy-experience",
                            options=[
                                {"label": "Extensive", "value": "extensive"},
                                {"label": "Some", "value": "some"},
                                {"label": "None", "value": "none"},
                            ],
                        ),
                    ],
                    sm=4,
                    width=12,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Continue to the test",
                    color="primary",
                    id="submit-personal-questionnaire",
                ),
                className="d-flex justify-content-center",
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="personal-questionnaire-error",
                    className="text-center text-danger mt-2",
                    hidden=True,
                )
            )
        ),
    ]
)
