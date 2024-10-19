from dash import Dash, page_container

import dash_bootstrap_components as dbc

from components.navbar import Navbar

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP],
)
server = app.server

app.layout = dbc.Container([Navbar, page_container])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050)
