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
import constants

ScatterCard = dmc.Card(
    children=[
        dmc.Title("Scatter 2D", order=2, c=constants.PRIMARY, ta="center"),
        dmc.RadioGroup(
            label="Color by",
            id="scatter-color-radio",
            children=dmc.Group(
                [dmc.Radio(l, value=k) for k, l in demographics_radio_options]
            ),
            size="md",
            value="gender",
            mb="xs",
        ),
        dmc.Group(
            children=[
                dmc.Select(
                    label="Select X-axis Variable:",
                    id="scatter-x-dropdown",
                    data=({"label": "Age", "value": "age"},)
                    + attachment_score_labels_values,
                    value="age",
                    size="md",
                ),
                dmc.Select(
                    label="Select Y-axis Variable:",
                    id="scatter-y-dropdown",
                    data=attachment_score_labels_values,
                    value="avoidant_score",
                    size="md",
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


