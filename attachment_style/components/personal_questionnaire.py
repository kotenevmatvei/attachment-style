import dash_bootstrap_components as dbc
from dash import html

PersonalQuestionnaire = dbc.Container(
    [
        # description
        dbc.Row(
            dbc.Col(
                html.Div(
                    """
                    Please fill out the following form to help us understand your background:
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
                        dbc.Input(type="number", id="age", min=0, max=100)
                    ],
                    width={"size": 4, "offset": 2}
                ),
                dbc.Col(
                    [
                        html.Div("Your relationship status:"),
                        dbc.Select(
                            id="relationship-status",
                            options=[
                                {"label": "Single", "value": "single"},
                                {"label": "In a relationship", "value": "relationship"},
                                {"label": "Married", "value": "married"},
                            ]
                        )
                    ],
                    width=4,
                )
            ],
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Your gender:"),
                        dbc.Select(
                            id="gender",
                            options=[
                                {"label": "Male", "value": "male"},
                                {"label": "Female", "value": "female"},
                                {"label": "Other", "value": "other"},
                            ]
                        )
                    ],
                    sm={"size": 4, "offset": 2},
                    width=8
                ),
                dbc.Col(
                    [
                        html.Div("Previous therapy experience:"),
                        dbc.Select(
                            id="therapy-experience",
                            options=[
                                {"label": "Yes", "value": "yes"},
                                {"label": "No", "value": "no"},
                            ]
                        )
                    ],
                    sm=4,
                    width=8
                )
            ],
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Continue to the test", color="primary", id="submit-personal-questionnaire"),
                className="d-flex justify-content-center"
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                        "Please fill out all fields before continuing",
                        id="personal-questionnaire-error", 
                        className="text-center text-danger mt-2", 
                        hidden=True
                )
            )
        )
    ]
)