from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from numpy import size
from data.options import demographics_labels_values, attachment_style_labels_values, demographics_radio_options
import pandas as pd
import plotly.express as px

BoxCard = dmc.Card(
    children=[
        dmc.Title("Box Plot", order=2, c="blue", ta="center"),
        dmc.Text("Select Demographic Variable:", size="lg"),
        dmc.RadioGroup(
            id="demographic-radio",
            children=dmc.Group([dmc.Radio(l, value=k) for k, l in demographics_radio_options]),
            size="lg",
            value="gender",
            mb="xs",
        ),
        dmc.Text("Select Attachment Style:", size="lg"),
        dmc.Select(
            id="attachment-style-dropdown-demographics",
            data=attachment_style_labels_values,
            value="avoidant_score",
            size="md",
        ),
        dcc.Graph(id="box-graph"),
    ],
    withBorder=True,
    shadow="md",
    radius="md",
    w=600,
)

# update box  lot graph
@callback(
    Output("box-graph", "figure"),
    [
        Input("demographic-radio", "value"),
        Input("attachment-style-dropdown-demographics", "value"),
        Input("data-store", "data"),
    ],
)
def update_box_graph(demographic, selected_style, data):
    fig = px.box(
        data,
        x=demographic,
        y=selected_style,
        title=f'{selected_style.split("_")[0].capitalize()} '
        f'Attachment Scores by {demographic.replace("_", " ").title()}',
    )
    fig.update_xaxes(title=demographic.replace("_", " ").title())
    fig.update_yaxes(
        title=selected_style.split("_")[0].capitalize() + " Attachment Score"
    )
    return fig
