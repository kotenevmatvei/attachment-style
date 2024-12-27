from dash import Dash, page_container, html, Output, Input

import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP],
)
server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dbc.NavLink("Attachment Style Test", href="/"),
                        html.Div(
                            [
                                html.Div(
                                    dbc.Stack(
                                        [
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
                                    className="border-0 d-sm-none",
                                    id="hamburger",
                                    n_clicks=0,
                                ),
                            ]
                        ),
                    ],
                    className="d-flex justify-content-between bg-light p-3 mb-4",
                ),
                html.Div(
                    page_container,
                    style={
                        "flex": "1",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                ),
                html.Div(
                    html.Footer(
                        "Created by Matvei Kotenev. Contact via kotenev.matvei@gmail.com.",
                    ),
                    style={
                        "backgroundColor": "#f1f1f1",
                        "position": "sticky",
                        "textAlign": "center",
                        "padding-top": "5px",
                        "padding-bottom": "5px",
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
                dbc.NavLink(
                    "Home",
                    href="/",
                    style={"cursor": "pointer"},
                    className="sidenav-link",
                ),
                dbc.NavLink(
                    "Assess Yourself",
                    href="/assess-yourself",
                    style={"cursor": "pointer"},
                    className="sidenav-link",
                ),
                dbc.NavLink(
                    "Assess Others",
                    href="/asses-others",
                    style={"cursor": "pointer"},
                    className="sidenav-link",
                ),
                dbc.NavLink(
                    "Dashboard",
                    href="/dashboard",
                    style={"cursor": "pointer"},
                    className="sidenav-link",
                ),
                dbc.NavLink(
                    "About",
                    href="/about",
                    style={"cursor": "pointer"},
                    className="sidenav-link",
                ),
            ],
            id="Sidenav",
        ),
    ],
)


@app.callback(
    Output("Sidenav", "className"),
    Input("hamburger", "n_clicks"),
)
def open_sidenav(hamburger_click):
    if hamburger_click:
        return "open"
    return ""


if __name__ == "__main__":
    # app.run_server(host="0.0.0.0", port=8050)
    app.run(debug=True)
