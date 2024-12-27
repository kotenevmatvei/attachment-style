from dash import Dash, page_container, html

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
                                    hidden=True,
                                ),
                                html.Button(
                                    html.I(className="bi bi-list"),
                                    className="border-0",
                                    hidden=False,
                                ),
                            ]
                        ),
                    ],
                    className="d-flex justify-content-between bg-light p-3 mb-4",
                ),
                html.Div(
                    page_container,
                    style={"flex": "1"},
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
                "padding-right": "15%",
                "padding-left": "15%",
            },
            className="body-response",
        ),
        html.Div(
            style={
                "height": "100%",
                "width": "0",
                "position": "fixed",
                "z-index": "1",
                "top": "0",
                "right": "0",
                "background-color": "#111",
                "overflow-x": "hidden",
                "padding-top": "60px",
                "transition": "0.5s",
            }
        ),
    ],
)
if __name__ == "__main__":
    # app.run_server(host="0.0.0.0", port=8050)
    app.run(debug=True)
