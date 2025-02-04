from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from data.options import (
    demographics_labels_values,
    attachment_style_labels_values,
    demographics_values,
)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


PieModal = dbc.Modal(
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

PieThumbnail = (
    html.Div(
        dcc.Graph(
            id="pie-thumbnail",
            config={"staticPlot": True},
            style={"cursor": "pointer"},
        ),
        id="pie-container",
        className="thumbnail",
    )
)


# GLOBAL PIE CHART
# toggle pie modal
@callback(
    Output("pie-modal", "is_open"),
    [Input("pie-container", "n_clicks"), Input("close-pie", "n_clicks")],
    State("pie-modal", "is_open"),
)
def toggle_pie_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update pie thumbnail
@callback(
    Output("pie-thumbnail", "figure"),
    [
        Input("global-pie-chart-dropdown-attachment-style", "value"),
        Input("global-pie-chart-dropdown-demographic", "value"),
        Input("data-store", "data"),
        Input("window-width", "data"),
    ],
)
def update_global_pie_thumbnail(
    attachment_style: str,
    demographic: str,
    data,
    window_width,
) -> go.Figure:
    answers_df = pd.DataFrame(data)
    options: tuple[str, ...] = tuple(
        option for option in demographics_values[demographic]
    )
    values: tuple[float, ...] = tuple(
        answers_df[answers_df[demographic] == option][attachment_style].mean()
        for option in options
    )

    if window_width[0] > 500:
        fig = px.pie(
            values=values,
            names=options,
            title="Global Pie Chart",
            width=300,
            height=250,
            # template="plotly_dark",
        )
        fig.update_layout(
            title_x=0.5,
            title_y=0.98,
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
    else:
        fig = px.pie(
            values=values,
            names=options,
            title="Global Pie Chart",
            width=165,
            height=180,
            # template="plotly_dark",
        )
        fig.update_layout(
            title_font_size=15,
            title_x=0.5,
            title_y=0.95,
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
        fig.update_traces(textinfo="none")

    return fig


# update pie graph
@callback(
    Output("pie-graph", "figure"),
    [
        Input("global-pie-chart-dropdown-attachment-style", "value"),
        Input("global-pie-chart-dropdown-demographic", "value"),
        Input("data-store", "data"),
    ],
)
def update_global_pie_graph(attachment_style: str, demographic: str, data) -> go.Figure:
    answers_df = pd.DataFrame(data)
    options: tuple[str, ...] = tuple(
        option for option in demographics_values[demographic]
    )
    values: tuple[float, ...] = tuple(
        answers_df[answers_df[demographic] == option][attachment_style].mean()
        for option in options
    )

    fig = px.pie(
        values=values,
        names=options,
        title=f"{attachment_style.replace('_', ' ').capitalize()} distribution"
        f" by {demographic.replace('_', ' ')}",
        # template="plotly_dark",
    )

    return fig
