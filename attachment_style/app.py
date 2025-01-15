from dash import Dash, page_container, html, Output, Input, dcc, clientside_callback

import dash_bootstrap_components as dbc

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
                dcc.Store(id="dimensions"),
                html.Div(id="dummy"),
                html.Div(
                    [
                        dbc.NavLink(
                            "Attachment Style Test", href="/", className="fs-5"
                        ),
                        html.Div(
                            [
                                html.Div(
                                    dbc.Stack(
                                        [
                                            dbc.NavLink(
                                                "Home",
                                                href="/",
                                                style={
                                                    "cursor": "pointer",
                                                    "margin-right": "4px",
                                                },
                                            ),
                                            dbc.NavLink(
                                                "Assess Yourself",
                                                href="/assess-yourself",
                                                id="assess-yourself",
                                                style={"cursor": "pointer"},
                                            ),
                                            dbc.NavLink(
                                                "Assess Others",
                                                href="/asses-others",
                                                id="asses-others",
                                                style={"cursor": "pointer"},
                                            ),
                                            dbc.NavLink(
                                                "Dashboard",
                                                href="/dashboard",
                                                style={"cursor": "pointer"},
                                            ),
                                            dbc.NavLink(
                                                "About",
                                                href="/about",
                                                style={"cursor": "pointer"},
                                            ),
                                        ],
                                        direction="horizontal",
                                        gap=3,
                                    ),
                                    className="navbar-large",
                                ),
                                html.Button(
                                    html.I(className="bi bi-list"),
                                    className="border-0 d-sm-none bg-transparent",
                                    id="hamburger",
                                    n_clicks=0,
                                ),
                            ]
                        ),
                    ],
                    className="d-flex justify-content-between align-items-center p-3 mb-4",
                ),
                html.Div(
                    page_container,
                    style={
                        "flex": "1",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                    className="page-container",
                ),
                html.Div(
                    html.Footer(
                        "Created by Matvei Kotenev. Contact via kotenev.matvei@gmail.com.",
                    ),
                    style={
                        "position": "sticky",
                        "textAlign": "center",
                        "padding-top": "5px",
                        "padding-bottom": "5px",
                        "font-size": "12px",
                    },
                ),
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
        html.Div(
            [
                html.I(
                    className="bi bi-x-lg sidenav-link bg-transparent pb-3",
                    id="close-sidenav-top",
                    n_clicks=0,
                ),
                dbc.NavLink(
                    "Home",
                    href="/",
                    id="home-sidenav",
                    style={"cursor": "pointer"},
                    className="sidenav-link",
                ),
                dbc.NavLink(
                    "Assess Yourself",
                    href="/assess-yourself",
                    id="assess-yourself-sidenav",
                    style={"cursor": "pointer"},
                    className="sidenav-link",
                ),
                dbc.NavLink(
                    "Assess Others",
                    href="/asses-others",
                    id="assess-others-sidenav",
                    style={"cursor": "pointer"},
                    className="sidenav-link",
                ),
                dbc.NavLink(
                    "Dashboard",
                    href="/dashboard",
                    id="dashboard-sidenav",
                    style={"cursor": "pointer"},
                    className="sidenav-link",
                ),
                dbc.NavLink(
                    "About",
                    href="/about",
                    id="about-sidenav",
                    style={"cursor": "pointer", "flex": "1"},
                    className="sidenav-link",
                ),
                dbc.NavLink(
                    "Close",
                    id="close-sidenav-bottom",
                    style={"cursor": "pointer", "padding-bottom": "20px"},
                    className="sidenav-link",
                ),
            ],
            id="Sidenav",
        ),
        dcc.Store(id="window-size"),
    ],
)


@app.callback(
    [
        Output("Sidenav", "className"),
        Output("opacity", "className"),
    ],
    Input("hamburger", "n_clicks"),
)
def open_sidenav(hamburger_click):
    if hamburger_click:
        return "open", "open"
    return "", ""


@app.callback(
    [
        Output("Sidenav", "className", allow_duplicate=True),
        Output("opacity", "className", allow_duplicate=True),
    ],
    [Input("close-sidenav-top", "n_clicks"), Input("close-sidenav-bottom", "n_clicks")],
    prevent_initial_call=True,
)
def fold_sidenavbar(close_top_click, close_bottom_click):
    # if home_click or yourself_click or others_click or dashboard_click or about_click:
    if close_top_click or close_bottom_click:
        return "", ""


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
        var h = window.innerHeight; 
        return [w, h]
    }
    """,
    Output("dimensions", "data"),
    Input("dummy", "n_clicks"),
)

@app.callback(
    Output("dummy","children"),
    Input("dimensions", "data")
)
def print_dimenstions(data):
    return data

if __name__ == "__main__":
    # app.run_server(host="0.0.0.0", port=8050)
    app.run(debug=True)
