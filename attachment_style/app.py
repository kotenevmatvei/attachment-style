from dash import Dash, page_container, html, Output, Input, dcc
import dash_bootstrap_components as dbc
from components.navbar import Navbar, NavbarMobile
from components.footer import Footer

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
