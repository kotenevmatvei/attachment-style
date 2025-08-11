from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from data.options import demographics_labels_values, attachment_style_labels_values
import pandas as pd
import plotly.express as px

ParallelCard = dmc.Card(
    [
        dmc.Title("Parllel Coordinates", order=2, c="blue", ta="center"),
        dmc.Text("Select Variables:", size="lg"),
        dmc.MultiSelect(
            id="parallel-categories-dropdown",
            data=demographics_labels_values,
            value=["gender", "therapy_experience"],
            size="lg",
        ),
        dmc.Text("Color By Attachment Style:", size="lg"),
        dmc.Select(
            id="parallel-color-dropdown",
            data=attachment_style_labels_values
            + ({"label": "Any", "value": "any"},),
            value="anxious_score",
            size="lg",
        ),
        dcc.Graph(id="parallel-graph"),
    ],
    withBorder=True,
    shadow="md",
    radius="md",
    w=600,
)


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
    if not selected_dims:
        selected_dims = ["gender"]
    if color_by == "any":
        fig = px.parallel_categories(
            data,
            dimensions=selected_dims,
            color_continuous_scale=px.colors.sequential.Inferno,
            title="Parallel Categories Diagram",
        )
    else:
        fig = px.parallel_categories(
            data,
            dimensions=selected_dims,
            color=color_by,
            color_continuous_scale=px.colors.sequential.Inferno,
            title="Parallel Categories Diagram",
        )
    return fig
