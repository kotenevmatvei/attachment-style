import dash_bootstrap_components as dbc
from dash import html

PersonalQuestionnairePartner = dbc.Container(
    [
        # description
        dbc.Row(
            dbc.Col(
                html.Div(
                    """
                    Please fill out the following form with regard to the person you are completing the test for
                    to your best knowledge:
                    """,
                ),
                className="text-center mb-2"
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Your age in years:"),
                        dbc.Input(type="number", id="age-partner", min=0, max=100)
                    ],
                    sm={"size": 4, "offset": 2},
                    width=12,
                ),
                dbc.Col(
                    [
                        html.Div("Your relationship status:"),
                        dbc.Select(
                            id="relationship-status-partner",
                            options=[
                                {"label": "Single", "value": "single"},
                                {"label": "In a relationship", "value": "relationship"},
                                {"label": "Married", "value": "married"},
                            ]
                        )
                    ],
                    sm=4,
                    width=12,
                )
            ],
            className="mb-4 mb-2-xs"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Your gender:"),
                        dbc.Select(
                            id="gender-partner",
                            options=[
                                {"label": "Male", "value": "male"},
                                {"label": "Female", "value": "female"},
                                {"label": "Other", "value": "other"},
                            ]
                        )
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
                                {"label": "Yes", "value": "yes"},
                                {"label": "No", "value": "no"},
                            ]
                        )
                    ],
                    sm=4,
                    width=12,
                )
            ],
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Continue to the test", color="primary", id="submit-personal-questionnaire-partner"),
                className="d-flex justify-content-center"
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                        "Please fill out all fields before continuing",
                        id="personal-questionnaire-error-partner", 
                        className="text-center text-danger mt-2", 
                        hidden=True
                )
            )
        )
    ]
)
