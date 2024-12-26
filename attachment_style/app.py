from dash import Dash, page_container, html

import dash_bootstrap_components as dbc

from components.navbar import Navbar
from components.footer import Footer

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP],
)
server = app.server

app.layout = dbc.Container(
    [
        Navbar,
        dbc.Row(
            dbc.Col(
                page_container,
            ),
            style={"flex": "1"},
        ),
        dbc.Row(
            dbc.Col(
                html.Footer(
                    "Created by Matvei Kotenev. Contact via kotenev.matvei@gmail.com.",
                    style={"margin": "0"}
                )
            ),
            style={
                "backgroundColor": "#f1f1f1",
                "position": "sticky",
                "textAlign": "center",
                "padding": "10px"
            },
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "column",
        "height": "100vh",
    },
)

if __name__ == "__main__":
    # app.run_server(host="0.0.0.0", port=8050)
    app.run(debug=True)
