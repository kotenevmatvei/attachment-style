from dash import register_page, html
import dash_bootstrap_components as dbc

register_page(__name__)


def layout(**kwargs):
    return dbc.Container(
        html.Div(
            "This is about page"
        )
    )
