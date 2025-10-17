import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc, Input, State, Output, callback
from data.options import (
    attachment_score_labels_values,
    demographics_labels_values,
    attachment_style_options,
    demographics_radio_options,
)
from dash_iconify import DashIconify
import constants

ScatterCard = dmc.Card(
    id="scatter-plot-card",
    children=[
        dmc.CardSection(
            dmc.SimpleGrid(
                cols=3,
                children=[
                    dmc.Space(w="xs"),
                    dmc.Center(
                        dmc.Title("Scatter Plot", id="scatter-plot-title", order=2, ta="center", c=constants.PRIMARY),
                    ),
                    dmc.Flex(
                        dmc.Button(
                            DashIconify(icon="material-symbols:help-outline", width=25, color=constants.PRIMARY),
                            id="scatter-info-modal-button",
                            variant="light",
                            radius="md"
                        ),
                        justify="right",
                        align="center",
                    )
                ]
            ),
            withBorder=True,
            p={"base": "xs", "sm": "md"},
            mb="xs",
        ),
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
            ],
            mb="xs",
        ),
        dcc.Graph(id="scatter-graph"),

        dmc.Modal(
            title=dmc.Title("Scatter Plot", order=3),
            id="scatter-info-modal",
            shadow="xl",
            padding=25,
            size="lg",
            children=[
                # dmc.Image(src="assets/scatter_info.png"),
                # dmc.Space(h="md"),
                dmc.Text(
                    "A scatter plot is a fundamental data visualization technique that displays the relationship between "
                    "two continuous variables using dots plotted on a coordinate system. This graphical method uses the "
                    "Cartesian plane to reveal patterns, trends, and correlations between variables by positioning each "
                    "data point according to its values on both the horizontal and vertical axes."
                ),
                dmc.Space(h="md"),
                dmc.Text("Key Components", fw="bold"),
                dmc.Space(h="md"),
                dmc.Text(
                    "The scatter plot consists of several essential elements that work together to display relationships "
                    "in data. The horizontal axis (X-axis) typically represents the independent variable - the factor "
                    "that researchers believe influences or causes changes in another variable. The vertical axis (Y-axis) "
                    "displays the dependent variable - the outcome that is expected to change based on the independent variable."
                ),
                dmc.Space(h="md"),
                dmc.Text(
                    "Each data point appears as a marker (dot, circle, or other symbol) positioned precisely where the "
                    "two variable values intersect on the coordinate plane. The collection of all these markers creates "
                    "the overall pattern that reveals the nature of the relationship between the variables."
                ),
                dmc.Space(h="md"),
                dmc.Text("Reading the Plot", fw="bold"),
                dmc.Space(h="md"),
                dmc.Text(
                    "Scatter plots make it straightforward to identify correlation patterns and their characteristics. "
                    "A positive correlation appears when data points trend upward from left to right, indicating that "
                    "as one variable increases, the other also increases. A negative correlation shows a downward trend, "
                    "where one variable increases as the other decreases."
                ),
                dmc.Space(h="md"),
                dmc.Text(
                    "The strength of correlation becomes apparent through how closely the points cluster around a potential "
                    "trend line - tightly grouped points indicate strong correlation, while widely scattered points suggest "
                    "weak correlation. When points show no clear pattern and appear randomly distributed, this indicates "
                    "null correlation or no meaningful relationship between the variables. Scatter plots also excel at "
                    "revealing outliers - unusual data points that fall far from the main pattern and may warrant further "
                    "investigation."
                ),
            ]
        )
    ],
    withBorder=True,
    shadow="md",
    radius="md",
    w=600,
)


