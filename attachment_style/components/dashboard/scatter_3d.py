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
import constants

Scatter3dCard = dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Title("Scatter 3D", order=2, c=constants.PRIMARY, ta="center"),
            withBorder=True, p="md", mb="xs",
        ),
        dmc.RadioGroup(
            label="Color by",
            id="scatter3d-color-radio",
            children=dmc.Group(
                [dmc.Radio(l, value=k) for k, l in demographics_radio_options]
            ),
            size="md",
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

