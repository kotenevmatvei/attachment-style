from dash import callback, Output, Input, State
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


@callback(
    Output("parallel-info-modal", "opened"),
    Input("parallel-info-modal-button", "n_clicks"),
    State("parallel-info-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_box_info_modal(n_clicks, opened):
    return not opened
