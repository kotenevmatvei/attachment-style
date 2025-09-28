from dash import callback, Output, Input, State
import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc

# update 3d scatter
@callback(
    Output("scatter3d-graph", "figure"),
    [
        Input("presented-data-store", "data"),
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

    fig.update_layout(
        scene_camera={
            "eye": {"x": 1.8, "y": 1.8, "z": 1.8},
            # "up": {"x": 0, "y": 2, "z": 0}
        }
    )

    if theme == "light":
        fig.update_layout(template="mantine_light")
    else:
        fig.update_layout(template="mantine_dark")

    return fig

@callback(
    Output("scatter-3d-info-modal", "opened"),
    Input("scatter-3d-info-modal-button", "n_clicks"),
    State("scatter-3d-info-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_box_info_modal(n_clicks, opened):
    return not opened
