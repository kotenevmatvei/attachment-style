from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from data.options import (
    demographics_labels_values,
    attachment_style_labels_values,
    demographics_radio_options,
)
from dash_iconify import DashIconify
import constants

Scatter3dCard = dmc.Card(
    id="scatter3d-plot-card",
    children=[
        dmc.CardSection(
            dmc.SimpleGrid(
                cols=3,
                children=[
                    dmc.Space(w="xs"),
                    dmc.Center(
                        dmc.Title("Scatter 3D", id="scatter-3d-plot-title", order=2, ta="center", c=constants.PRIMARY),
                    ),
                    dmc.Flex(
                        dmc.Button(
                            DashIconify(icon="material-symbols:help-outline", width=25, color=constants.PRIMARY),
                            id="scatter-3d-info-modal-button",
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
            id="scatter3d-color-radio",
            children=dmc.Group(
                [dmc.Radio(l, value=k) for k, l in demographics_radio_options]
            ),
            size="md",
            value="gender",
            mb="xs",
        ),
        dcc.Graph(id="scatter3d-graph"),

        dmc.Modal(
            title=dmc.Title("Scatter 3D Plot", order=3),
            id="scatter-3d-info-modal",
            shadow="xl",
            padding=25,
            size="lg",
            children=[
                # dmc.Image(src="assets/scatter_3d_info.png"),
                # dmc.Space(h="md"),
                dmc.Text(
                    "A 3D scatter plot is an advanced data visualization technique that displays relationships between "
                    "three continuous variables simultaneously by plotting data points in three-dimensional space. This "
                    "powerful extension of the traditional scatter plot uses a coordinate system with X, Y, and Z axes "
                    "to reveal complex multivariate patterns that cannot be observed in two-dimensional representations."
                ),
                dmc.Space(h="md"),
                dmc.Text("Key Components", fw="bold"),
                dmc.Space(h="md"),
                dmc.Text(
                    "The 3D scatter plot utilizes three perpendicular axes to create a three-dimensional coordinate system. "
                    "The X-axis (horizontal), Y-axis (vertical), and Z-axis (depth) each represent a different variable, "
                    "allowing researchers to examine how three factors interact with one another. Each data point appears "
                    "as a marker positioned precisely where the three variable values intersect in the three-dimensional "
                    "space."
                ),
                dmc.Space(h="md"),
                dmc.Text(
                    "Many 3D scatter plots incorporate a fourth dimension through visual properties such as marker color, "
                    "size, or shape, effectively allowing the visualization of four variables simultaneously. Navigation "
                    "controls are essential components that enable users to rotate, zoom, and change viewing angles to "
                    "explore the data from different perspectives."
                ),
                dmc.Space(h="md"),
                dmc.Text("Reading the Plot", fw="bold"),
                dmc.Space(h="md"),
                dmc.Text(
                    "3D scatter plots excel at revealing complex relationships and patterns that remain hidden in "
                    "traditional two-dimensional visualizations. Strong correlations between variables become apparent "
                    "when data points cluster together to form recognizable patterns, lines, or surfaces in the "
                    "three-dimensional space. When points appear randomly distributed throughout the 3D space, this "
                    "indicates weak or no correlation between the variables. "
                ),
                dmc.Space(h="md"),
                dmc.Text(
                    "The added dimensionality makes 3D scatter plots particularly effective for identifying clusters and "
                    "groupings that might not be visible in 2D projections. Outliers become more apparent as isolated "
                    "points that deviate significantly from the main data cloud, often revealing anomalies or interesting "
                    "observations that warrant further investigation. The ability to rotate and examine the plot from "
                    "multiple angles allows analysts to discover relationships and structures that might be obscured "
                    "from a single viewing perspective."
                ),
            ]
        )
    ],
    withBorder=True,
    shadow="md",
    radius="md",
    w=600,
)

