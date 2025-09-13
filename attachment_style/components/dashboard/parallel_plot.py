from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from data.options import demographics_labels_values, attachment_style_labels_values
import pandas as pd
import plotly.express as px
import constants

dmc.add_figure_templates()

ParallelCard = dmc.Card(
    [
        dmc.CardSection(
            dmc.Title("Parllel Coordinates", order=2, c=constants.PRIMARY, ta="center"),
            withBorder=True, p="md", mb="xs",
        ),
        dmc.MultiSelect(
            label="Select Variables",
            id="parallel-categories-dropdown",
            data=demographics_labels_values,
            value=["gender", "therapy_experience"],
            size="md",
        ),
        dmc.Select(
            label="Color By Attachment Style:",
            id="parallel-color-dropdown",
            data=attachment_style_labels_values
            + ({"label": "Any", "value": "any"},),
            value="anxious_score",
            size="md",
            mb="xs",
        ),
        dcc.Graph(id="parallel-graph"),
    ],
    withBorder=True,
    shadow="md",
    radius="md",
    w=600,
)


