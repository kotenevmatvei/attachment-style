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
                        className="d-flex text-center justify-content-center",
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
                            that of your partner or someone else. [Test Yourself](/test-yourself) is a rather 
                            subjective version that one can only really answer for oneself. 
                            [Test Your Partner](/test-your-partner) offers more behavior-based questions that can 
                            be answered with regard to someone else - *as well as yourself*.  
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
                            "Test Yourself",
                            href="/test-yourself",
                            color="primary",
                            className="d-flex justify-content-center",
                        ),
                        width=6,
                        sm={"size":3, "offset":3}
                    ),
                    
                    dbc.Col(
                        dbc.Button(
                            "Test Your Partner",
                            href="/test-your-partner",
                            color="primary",
                            className="d-flex justify-content-center",
                        ),
                        width=6,
                        sm={"size":3, "offset":0}
                    ),
                ]
            )
        ]   
    )