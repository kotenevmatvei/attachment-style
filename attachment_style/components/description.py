import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback

Description = html.Div(
    dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H3("Test Yourself", id="subject-title"),
                    className="d-flex justify-content-center"
                )
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Markdown(
                        """
                        Please evaluate how much you can relate to the following statements on the scale from 0 to 10.
                        """,
                        className="text-center"
                    ),
                    width=12,
                    sm=8,
                    className="mb-4 mx-auto"
                )
            )  
        ]
    )
)

@callback(
    Output("subject-title", "children"),
    [
        Input("questions-storage", "data")
    ]
)
def update_subject_title(questions):
    if len(questions) == 42:
        return "Test Yourself"
    else:
        return "Test Your Partner"