from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from data.options import (
    demographics_labels_values,
    attachment_style_labels_values,
    demographics_radio_options,
)
import pandas as pd
import plotly.express as px

Scatter3dCard = dmc.Card(
    children=[
        dmc.Title("Scatter 3D", order=2, c="blue", ta="center"),
        dmc.Text("Color by", size="lg"),
        dmc.RadioGroup(
            id="scatter3d-color-radio",
            children=dmc.Group(
                [dmc.Radio(l, value=k) for k, l in demographics_radio_options]
            ),
            size="lg",
            value="gender",
            mb=0,
        ),
        dcc.Graph(id="scatter3d-graph"),
    ],
    withBorder=True,
    shadow="md",
    radius="md",
    w=600,
)


# update 3d scatter
@callback(
    Output("scatter3d-graph", "figure"),
    [Input("data-store", "data"), Input("scatter3d-color-radio", "value")],
)
def update_scatter3d_graph(data, color_value):
    data = pd.DataFrame(data)
    fig = px.scatter_3d(
        data,
        x="anxious_score",
        y="avoidant_score",
        z="secure_score",
        color=color_value,
        color_continuous_scale=px.colors.sequential.Viridis,
        title="3D View of Attachment Dimensions",
        labels={
            "anxious_score": "Anxiety Score",
            "avoidant_score": "Avoidance Score",
            "secure_score": "Security Score",
        },
    )

    # fig.update_layout(
    #     scene=dict(
    #         xaxis=dict(backgroundcolor="rgba(0, 0, 0, 0)"),
    #         yaxis=dict(backgroundcolor="rgba(0, 0, 0, 0)"),
    #         zaxis=dict(backgroundcolor="rgba(0, 0, 0, 0)"),
    #     ),
    #     margin=dict(l=0, r=0, b=0, t=40) # Adjust margins
    # )

    return fig
