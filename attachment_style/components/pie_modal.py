from dash import html, dcc
import dash_bootstrap_components as dbc
from data.options import demographics_labels_values, attachment_style_labels_values

PieModal = (
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Global Pie Chart")),
            dbc.ModalBody(
                [
                    html.Label("Select the attachment style"),
                    dcc.Dropdown(
                        id="global-pie-chart-dropdown-attachment-style",
                        options=attachment_style_labels_values,
                        value="anxious_score",
                    ),
                    html.Label("Select the demographic"),
                    dcc.Dropdown(
                        id="global-pie-chart-dropdown-demographic",
                        options=demographics_labels_values,
                        value="gender",
                    ),
                    dcc.Graph(id="pie-graph"),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-pie",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="pie-modal",
        size="lg",
        is_open=False,
    )
)
