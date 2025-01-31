from dash import register_page, html, dcc
import dash_bootstrap_components as dbc

register_page(__name__, path="/")


def layout(**kwargs):
    return dbc.Container(
        [
            # header
            dbc.Row(
                dbc.Col(
                    html.H3(
                        "Welcome to the Attachment Style Quiz!",
                        className="d-flex text-center mb-4 justify-content-center",
                    ),
                )
            ),
            dbc.Row(
                dbc.Col(
                    [
                        dcc.Markdown(
                            """                
                            Attachment style theory is a psychological model that describes 
                            how we interact with others in our relationships.\n                 
                            This test includes 
                            two questionnaires to help you determine your attachment style, or 
                            that of your partner or someone else. [Assess Yourself](/assess-yourself) is a rather 
                            subjective version that one can only really answer for oneself. 
                            [Assess Others](/asses-others) offers more behavior-based questions that can 
                            be answered with regard to someone else - *as well as yourself*. At the end
                            you can download a pdf with all your answers.\n  
                            The dashboard page presents the data collected so far
                            visualized in multiple plots.
                            """,
                        )
                    ],
                    width=12,
                    xl=8,
                    className="mx-auto",
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "Assess Yourself",
                            href="/assess-yourself",
                            color="primary",
                            className="d-flex justify-content-center",
                        ),
                        width=6,
                        sm={"size": 3, "offset": 3},
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Assess Others",
                            href="/asses-others",
                            color="primary",
                            className="d-flex justify-content-center",
                        ),
                        width=6,
                        sm={"size": 3, "offset": 0},
                    ),
                ],
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Button(
                        "Dashboard",
                        href="/dashboard",
                        color="primary",
                        className="d-flex justify-content-center",
                    ),
                    width=12,
                    sm={"size": 4, "offset": 4},
                ),
                className="mt-3",
            ),
        ],
    )
