import dash_bootstrap_components as dbc
from dash import html, dcc
from data.options import attachment_score_labels_values, demographics_labels_values

ScatterModal = (
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Scatter Plot")),
            dbc.ModalBody(
                [
                    html.Label("Select X-axis Variable:"),
                    dcc.Dropdown(
                        id="scatter-x-dropdown",
                        options=({"label": "Age", "value": "age"},)
                        + attachment_score_labels_values,
                        value="age",
                    ),
                    html.Label("Select Y-axis Variable:"),
                    dcc.Dropdown(
                        id="scatter-y-dropdown",
                        options=attachment_score_labels_values,
                        value="avoidant_score",
                    ),
                    html.Div(
                        "Please choose the Y variable different from X",
                        id="scatter-y-warning",
                        style={"color": "red"},
                        hidden=True,
                    ),
                    html.Label("Color By:"),
                    dcc.Dropdown(
                        id="scatter-color-dropdown",
                        options=({"label": "None", "value": "None"},)
                        + demographics_labels_values,
                        value="gender",
                    ),
                    dcc.Graph(id="scatter-graph"),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-scatter",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="scatter-modal",
        size="lg",
        is_open=False,
    )
)
