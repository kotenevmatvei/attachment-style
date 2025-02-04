from dash import html, dcc
import dash_bootstrap_components as dbc
from data.options import demographics_labels_values, attachment_style_labels_values

SpiderModal = (
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Spider Chart")),
            dbc.ModalBody(
                [
                    html.Label("Select the attachment style:"),
                    dcc.Dropdown(
                        id="spider-attachment-style-dropdown",
                        options=attachment_style_labels_values,
                        clearable=False,
                        value="anxious_score",
                    ),
                    html.Label(
                        "Select Demographic Grouping for the shape " "(at least one):"
                    ),
                    dcc.Dropdown(
                        id="spider-shape-dropdown",
                        options=demographics_labels_values,
                        value=["gender", "relationship_status"],
                        clearable=False,
                        multi=True,
                    ),
                    html.Label("Select Demographic Grouping for the color:"),
                    dcc.Dropdown(
                        id="spider-color-dropdown",
                        options=demographics_labels_values,
                        value=["therapy_experience"],
                        multi=True,
                    ),
                    dcc.Graph(id="spider-chart"),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-spider",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="spider-modal",
        size="lg",
        is_open=False,
    )
)
