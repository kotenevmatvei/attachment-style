import dash_bootstrap_components as dbc
from dash import html

DemographicQuestionnaireOthers = dbc.Container(
    [
        # description
        dbc.Row(
            dbc.Col(
                html.Div(
                    """
                    Please fill out the following form (to your best knowledge) with 
                    regard to the person you are completing the test for:
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
                        dbc.Input(type="number", id="age-partner"),
                    ],
                    sm={"size": 4, "offset": 2},
                    width=12,
                ),
                dbc.Col(
                    [
                        html.Div("Relationship status:"),
                        dbc.Select(
                            id="relationship-status-partner",
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
                            id="gender-partner",
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
                            id="therapy-experience-partner",
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
                    id="submit-personal-questionnaire-partner",
                ),
                className="d-flex justify-content-center",
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="personal-questionnaire-error-partner",
                    className="text-center text-danger mt-2",
                    hidden=True,
                )
            )
        ),
    ]
)
