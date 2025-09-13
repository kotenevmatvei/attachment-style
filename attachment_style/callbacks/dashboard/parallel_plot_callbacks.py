from dash import callback, Output, Input
import plotly.express as px

# update parallel graph
@callback(
    Output("parallel-graph", "figure"),
    [
        Input("parallel-categories-dropdown", "value"),
        Input("parallel-color-dropdown", "value"),
        Input("presented-data-store", "data"),
        Input("mantine-provider", "forceColorScheme"),
    ],
)
def update_parallel_graph(selected_dims, color_by, data, theme):
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
            template="mantine_light",
        )
    if theme == "light":
        fig.update_layout(template="mantine_light")
    else:
        fig.update_layout(template="mantine_dark")
    return fig
