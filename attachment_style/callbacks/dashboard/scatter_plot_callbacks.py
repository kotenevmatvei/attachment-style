from dash import callback, Output, Input, State
import plotly.express as px

# update scatter graph
@callback(
    Output("scatter-graph", "figure"),
    [
        Input("scatter-x-dropdown", "value"),
        Input("scatter-y-dropdown", "value"),
        Input("scatter-color-radio", "value"),
        Input("scatter-color-select", "value"),
        Input("presented-data-store", "data"),
        Input("mantine-provider", "forceColorScheme"),
        Input("window-width", "data"),
    ],
)
def update_scatter_graph(x_var, y_var, color_var_radio, color_var_select, data, theme, window_width):
    if y_var is None:
        return px.scatter([]), False

    if window_width < 500:
        color_var = color_var_select # on mobile
    else:
        color_var = color_var_radio # on desktop

    if color_var == "None":
        fig = px.scatter(
            data,
            x=x_var,
            y=y_var,
            title=f"{y_var.split('_')[0].capitalize()} vs {x_var.capitalize()}",
        )
    else:
        fig = px.scatter(
            data,
            x=x_var,
            y=y_var,
            color=color_var,
            title=f"{y_var.split('_')[0].capitalize()} vs {x_var.capitalize()} Colored "
                  f"by {color_var.replace('_', ' ').title()}",
        )
    fig.update_xaxes(title=x_var.replace("_", " ").title())
    fig.update_yaxes(title=y_var.replace("_", " ").title())

    if window_width < 500:
        fig.update_layout(
            title="",
            width=350,
            height=330,
            margin=dict(l=0, r=0, t=20, b=0)
        )

    if theme == "light":
        fig.update_layout(template="mantine_light")
    else:
        fig.update_layout(template="mantine_dark")

    return fig

@callback(
    Output("scatter-info-modal", "opened"),
    Input("scatter-info-modal-button", "n_clicks"),
    State("scatter-info-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_box_info_modal(n_clicks, opened):
    return not opened
