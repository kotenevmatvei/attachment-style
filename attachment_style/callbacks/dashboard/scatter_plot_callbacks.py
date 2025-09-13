from dash import callback, Output, Input
import plotly.express as px

# update scatter graph
@callback(
    Output("scatter-graph", "figure"),
    [
        Input("scatter-x-dropdown", "value"),
        Input("scatter-y-dropdown", "value"),
        Input("scatter-color-radio", "value"),
        Input("presented-data-store", "data"),
        Input("mantine-provider", "forceColorScheme")
    ],
)
def update_scatter_graph(x_var, y_var, color_var, data, theme):
    if y_var is None:
        return px.scatter([]), False
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

    if theme == "light":
        fig.update_layout(template="mantine_light")
    else:
        fig.update_layout(template="mantine_dark")

    return fig
