from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from data.options import demographics_labels_values, attachment_style_labels_values
import pandas as pd
import plotly.express as px

ParallelModal = dbc.Modal(
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


ParallelThumbnail = (
    html.Div(
        dcc.Graph(
            id="parallel-thumbnail",
            config={"staticPlot": True},
            style={"cursor": "pointer"},
        ),
        id="parallel-container",
        className="thumbnail",
    )
)


# toggle parallel modal
@callback(
    Output("parallel-modal", "is_open"),
    [Input("parallel-container", "n_clicks"), Input("close-parallel", "n_clicks")],
    State("parallel-modal", "is_open"),
)
def toggle_parallel_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update parallel thumbnail
@callback(
    Output("parallel-thumbnail", "figure"),
    [
        Input("parallel-categories-dropdown", "value"),
        Input("parallel-color-dropdown", "value"),
        Input("data-store", "data"),
        Input("window-width", "data"),
    ],
)
def update_parallel_thumnail(selected_dims, color_by, data, window_width):
    answers_df = pd.DataFrame(data)
    if not selected_dims:
        selected_dims = ["gender"]
    if window_width[0] > 500:
        if color_by == "any":
            fig = px.parallel_categories(
                answers_df,
                dimensions=selected_dims,
                color_continuous_scale=px.colors.sequential.Inferno,
                title="Parallel Categories Diagram",
            )
        else:
            fig = px.parallel_categories(
                answers_df,
                dimensions=selected_dims,
                color=color_by,
                color_continuous_scale=px.colors.sequential.Inferno,
                title="Parallel Categories Diagram",
                width=300,
                height=250,
            )
        fig.update_layout(
            title_x=0.5,
            title_y=0.98,
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
        fig.update_coloraxes(showscale=False)
        for dim in fig.data[0]["dimensions"]:
            dim["label"] = ""
    else:
        if color_by == "any":
            fig = px.parallel_categories(
                answers_df,
                dimensions=selected_dims,
                color_continuous_scale=px.colors.sequential.Inferno,
                title="Parallel Categories Diagram",
            )
        else:
            fig = px.parallel_categories(
                answers_df,
                dimensions=selected_dims,
                color=color_by,
                color_continuous_scale=px.colors.sequential.Inferno,
                title="Parallel Categories",
                width=175,
                height=175,
            )
        fig.update_layout(
            title_font_size=15,
            title_x=0.5,
            title_y=0.95,
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
        fig.update_coloraxes(showscale=False)
        for dim in fig.data[0]["dimensions"]:
            dim["label"] = ""
        fig.update_traces({"tickfont": {"size": 1, "color": "white"}})
    return fig


# update parallel graph
@callback(
    Output("parallel-graph", "figure"),
    [
        Input("parallel-categories-dropdown", "value"),
        Input("parallel-color-dropdown", "value"),
        Input("data-store", "data"),
    ],
)
def update_parallel_graph(selected_dims, color_by, data):
    answers_df = pd.DataFrame(data)
    if not selected_dims:
        selected_dims = ["gender"]
    if color_by == "any":
        fig = px.parallel_categories(
            answers_df,
            dimensions=selected_dims,
            color_continuous_scale=px.colors.sequential.Inferno,
            title="Parallel Categories Diagram",
        )
    else:
        fig = px.parallel_categories(
            answers_df,
            dimensions=selected_dims,
            color=color_by,
            color_continuous_scale=px.colors.sequential.Inferno,
            title="Parallel Categories Diagram",
        )
    return fig
