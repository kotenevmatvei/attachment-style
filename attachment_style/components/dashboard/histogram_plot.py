import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Output, Input, State
from data.options import attachment_style_labels_values
import pandas as pd
import plotly.express as px

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

HistogramThumbnail = html.Div(
    dcc.Graph(
        id="histogram-thumbnail",
        config={"staticPlot": True},
        style={"cursor": "pointer"},
    ),
    id="histogram-container",
    className="thumbnail",
)


# HISTOGRAM
# toggle histgram modal
@callback(
    Output("histogram-modal", "is_open"),
    [Input("histogram-container", "n_clicks"), Input("close-histogram", "n_clicks")],
    State("histogram-modal", "is_open"),
)
def toggle_histogram_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update histogram thumbnail
@callback(
    Output("histogram-thumbnail", "figure"),
    [
        Input("attachment-style-dropdown-histo", "value"),
        Input("data-store", "data"),
        Input("window-width", "data"),
    ],
)
def update_histo_thumbnail(selected_style, data, window_width):
    if window_width[0] > 500:
        fig = px.histogram(
            data,
            x=selected_style,
            nbins=20,
            title="Histogram",
            width=300,
            height=250,
        )
        fig.update_layout(
            title_x=0.57,
            title_y=0.98,
            xaxis_title="",
            yaxis_title="",
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
            paper_bgcolor="#F5F5F4",
        )
    else:
        fig = px.histogram(
            data,
            x=selected_style,
            nbins=20,
            title="Histogram",
            width=175,
            height=175,
        )
        fig.update_layout(
            title_font_size=15,
            title_x=0.59,
            title_y=0.95,
            xaxis_title="",
            yaxis_title="",
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
            paper_bgcolor="#F5F5F4",
        )
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
    return fig


# update histogram modal
@callback(
    Output("histogram-graph", "figure"),
    [Input("attachment-style-dropdown-histo", "value"), Input("data-store", "data")],
)
def update_histo_modal(selected_style, data):
    fig = px.histogram(
        data,
        x=selected_style,
        nbins=20,
        title=f'Distribution of {selected_style.split("_")[0].capitalize()} '
        f'Attachment Scores',
    )
    fig.update_layout(
        xaxis_title=selected_style.split("_")[0].capitalize() + " Attachment Score",
        yaxis_title="Count",
    )
    return fig
