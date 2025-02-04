from dash import html, dcc
import dash_bootstrap_components as dbc
from data.options import demographics_labels_values, attachment_style_labels_values

ParallelModal = (
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Parallel Categories Plot")),
            dbc.ModalBody(
                [
                    html.Label("Select Variables:"),
                    dcc.Dropdown(
                        id="parallel-categories-dropdown",
                        options=demographics_labels_values,
                        value=["gender", "therapy_experience"],
                        multi=True,
                    ),
                    html.Label("Color By Attachment Style:"),
                    dcc.Dropdown(
                        id="parallel-color-dropdown",
                        options=attachment_style_labels_values
                        + ({"label": "Any", "value": "any"},),
                        value="secure_score",
                    ),
                    dcc.Graph(id="parallel-graph"),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-parallel",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="parallel-modal",
        size="lg",
        is_open=False,
    )
)
