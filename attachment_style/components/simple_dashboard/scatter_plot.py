import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc, Input, State, Output, callback
from data.options import (
    attachment_score_labels_values,
    demographics_labels_values,
    attachment_style_options,
    demographics_radio_options,
)
import pandas as pd
import plotly.express as px

ScatterCard = dmc.Card(
    children=[
        dmc.Title("Scatter 2D", order=2, c="blue", ta="center"),
        dmc.Text("Color by", size="lg"),
        dmc.RadioGroup(
            id="scatter-color-radio",
            children=dmc.Group(
                [dmc.Radio(l, value=k) for k, l in demographics_radio_options]
            ),
            size="lg",
            value="gender",
            mb="xs",
        ),
        dmc.Group(
            children=[
                dmc.Stack(
                    children=[
                        dmc.Text("Select X-axis Variable:", size="lg"),
                        dmc.Select(
                            id="scatter-x-dropdown",
                            data=({"label": "Age", "value": "age"},)
                            + attachment_score_labels_values,
                            value="age",
                            size="md",
                        ),
                    ],
                    gap=0,
                ),
                dmc.Stack(
                    children=[
                        dmc.Text("Select Y-axis Variable:", size="lg"),
                        dmc.Select(
                            id="scatter-y-dropdown",
                            data=attachment_score_labels_values,
                            value="avoidant_score",
                            size="md",
                        ),
                    ],
                    gap=0,
                ),
            ]
        ),
        dcc.Graph(id="scatter-graph"),
    ],
    withBorder=True,
    shadow="md",
    radius="md",
    w=600,
)


# update scatter graph
@callback(
    Output("scatter-graph", "figure"),
    [
        Input("scatter-x-dropdown", "value"),
        Input("scatter-y-dropdown", "value"),
        Input("scatter-color-radio", "value"),
        Input("data-store", "data"),
    ],
)
def update_scatter_graph(x_var, y_var, color_var, data):
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
    return fig
