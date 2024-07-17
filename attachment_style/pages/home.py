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
                        className="d-flex justify-content-center",
                    ),               
                )   
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Markdown(
                        """                
                        Attachment style theory is a psychological model that describes the
                        way we interact with others in our relationships. This test offers
                        two questionnaires to help you determine your attachment style
                        
                        """,
                    ),
                    width=12,
                    xl=10,
                    className="mx-auto",
                )
            ),
        ]   
    )