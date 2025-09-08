from dash import callback, Output, Input
import plotly.express as px
import pandas as pd

# update 3d scatter
@callback(
    Output("scatter3d-graph", "figure"),
    [
        Input("data-store", "data"),
        Input("scatter3d-color-radio", "value"),
        Input("mantine-provider", "forceColorScheme")
    ],
)
def update_scatter3d_graph(data, color_value, theme):
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

    if theme == "light":
        fig.update_layout(template="mantine_light")
    else:
        fig.update_layout(template="mantine_dark")

    return fig
