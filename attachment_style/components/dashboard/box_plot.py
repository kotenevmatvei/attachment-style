import dash_mantine_components as dmc
from dash import dcc

import constants
from data.options import attachment_style_labels_values, demographics_radio_options

dmc.add_figure_templates()

BoxCard = dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Title("Box Plot", order=2, ta="center", c=constants.PRIMARY),
            withBorder=True, p="md", mb="xs",
        ),
        # dmc.CardSection("Box Plot", withBorder=True, p="md", c=constants.PRIMARY),
        dmc.RadioGroup(
            label="Select demographic variable",
            id="demographic-radio",
            children=dmc.Group([dmc.Radio(l, value=k) for k, l in demographics_radio_options]),
            size="md",
            value="gender",
            mb="xs",
        ),
        dmc.Select(
            label="Select attachment style",
            id="attachment-style-dropdown-demographics",
            data=attachment_style_labels_values,
            value="avoidant_score",
            size="md",
            mb="xs",
        ),
        dcc.Graph(id="box-graph"),
    ],
    withBorder=True,
    shadow="md",
    radius="md",
    w=600,
)
