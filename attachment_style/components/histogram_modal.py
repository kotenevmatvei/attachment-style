import dash_bootstrap_components as dbc
from dash import dcc, html
from data.options import attachment_style_labels_values

HistogramModal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Histogram")),
        dbc.ModalBody(
            [
                html.Label("Select Attachment Style:"),
                dcc.Dropdown(
                    id="attachment-style-dropdown-histo",
                    options=attachment_style_labels_values,
                    value="avoidant_score",
                ),
                dcc.Graph(id="histogram-graph"),
            ]
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Close",
                id="close-histogram",
                className="ms-auto",
                n_clicks=0,
            )
        ),
    ],
    id="histogram-modal",
    size="lg",
    is_open=False,
)
