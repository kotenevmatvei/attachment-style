import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, callback, register_page

register_page(__name__, path="/dashboard_modal")


def layout(**kwargs):
    return html.Div(
        [
            dbc.Button("Open modal", id="open", n_clicks=0),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Header")),
                    dbc.ModalBody("This is the content of the modal"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
                    ),
                ],
                id="modal",
                is_open=False,
            ),
        ]
    )


@callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
