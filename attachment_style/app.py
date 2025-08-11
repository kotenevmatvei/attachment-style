from dash import Dash, page_container, html, Output, Input, dcc
import dash_bootstrap_components as dbc
from components.navbar import Navbar, NavbarMobile
from components.footer import Footer
import plotly.graph_objects as go
import plotly.io as pio

import logging

logging.basicConfig(
    level=logging.INFO,
    # format="{asctime} - {levelname} - {filename} - {funcName} - {message}",
    format="APP: {levelname} - {filename} - {funcName} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

logger = logging.getLogger(__name__)

# since with freakin kaleido 1.0.0. upgrade we cannot create a persistant chromium
# process, it starts up everytime one exports a picture - and closes after that...
# this way we at least cache it on the startup, so that the first download doesn't take
# 8 seconds or so...
def prewarm_kaleido():
    logger.info("\nPrewarming freakin kaleido")
    fig = go.Figure(go.Bar(y=[1, 2, 3]))
    try:
        pio.write_image(fig, "/tmp/kaleido_warmup.png", width=100, height=100)
        logger.info("\nDone prewarming freakin kaleido")
    except Exception:
        pass
        logger.error("\Failed prewarming freakin kaleido")

prewarm_kaleido()

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP],
)
server = app.server

app.layout = html.Div(
    [
        html.Div(id="opacity"),
        html.Div(
            [
                html.Div(id="dummy"),
                Navbar,
                html.Div(
                    page_container,
                    style={
                        "flex": "1",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                    className="page-container",
                ),
                Footer,
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "height": "100vh",
                "padding-right": "10%",
                "padding-left": "10%",
            },
            className="body-response",
            id="main",
        ),
        NavbarMobile,
        dcc.Store(id="window-width"),
    ],
)


# add event listener for window resizing
app.clientside_callback(
    """
    function(trigger) {
        function dummyClick() {
            document.getElementById('dummy').click()
        };
        
        window.addEventListener('resize', dummyClick)
        return window.dash_clientside.no_update
    }
    """,
    Output("dummy", "style"),
    Input("dummy", "style"),
)

# store current dimension in store
app.clientside_callback(
    """
    function updateStore(click) {
        var w = window.innerWidth;
        return [w]
    }
    """,
    Output("window-width", "data"),
    Input("dummy", "n_clicks"),
)

@app.callback(
    [
        Output("Sidenav", "className", allow_duplicate=True),
        Output("opacity", "className", allow_duplicate=True),
    ],
    Input("opacity", "n_clicks"),
    prevent_initial_call=True,
)
def fold_navbar_mobile_when_clicked_outside(click):
    return "", ""



if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080)
    # app.run(debug=True)
