from dash import html, dcc, callback, Input, Output, State
# import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from data.options import demographics_labels_values, attachment_style_labels_values
from dash_iconify import DashIconify
import constants

dmc.add_figure_templates()

ParallelCard = dmc.Card(
    id="parallel-plot-card",
    children=[
        dmc.CardSection(
            dmc.Flex(
                justify="space-between",
                children=[
                    dmc.Space(w="xl"),
                    dmc.Center(
                        [
                            dmc.Space(w="xl"),
                            dmc.Title("Parallel Coordinates", id="parallel-plot-title", order=2, ta="center", c=constants.PRIMARY),
                        ]
                    ),
                    dmc.Button(
                        DashIconify(icon="material-symbols:help-outline", width=25,
                                    color=constants.PRIMARY),
                        id="parallel-info-modal-button",
                        variant="light",
                        radius="md",
                    ),
                ],
            ),
            withBorder=True,
            p={"base": "xs", "sm": "md"},
            mb="xs",
        ),
        dmc.MultiSelect(
            label="Select Variables",
            id="parallel-categories-dropdown",
            data=demographics_labels_values,
            value=["gender", "therapy_experience"],
            size={"base": "sm", "sm": "md"},
        ),
        dmc.Select(
            label="Attachment Style:",
            id="parallel-color-dropdown",
            data=attachment_style_labels_values
            + ({"label": "Any", "value": "any"},),
            value="anxious_score",
            size={"base": "sm", "sm": "md"},
            mb="xs",
            allowDeselect=False,
        ),
        dcc.Graph(id="parallel-graph"),

        dmc.Modal(
            title=dmc.Title("Parallel Coordinates Chart", order=3),
            id="parallel-info-modal",
            shadow="xl",
            padding=25,
            size="lg",
            children=[
                # dmc.Image(src="assets/parallel_info.jpg"),
                dmc.Text(
                    "A parallel coordinates chart is an advanced data visualization technique designed specifically for "
                    "displaying relationships between multiple variables simultaneously by representing each variable as "
                    "a parallel vertical axis and connecting data points with lines. This powerful method excels at "
                    "revealing patterns, correlations, and clusters in high-dimensional datasets that would be "
                    "impossible to visualize effectively using traditional two-dimensional scatter plots."
                ),
                dmc.Space(h="md"),
                dmc.Text("Key Components", fw="bold"),
                dmc.Space(h="md"),
                dmc.Text(
                    "The parallel coordinates chart consists of two fundamental elements that work together to create a "
                    "comprehensive multivariate visualization. Parallel axes are vertical lines arranged side by side, "
                    "with each axis representing a different variable or dimension from the dataset. These axes are "
                    "typically evenly spaced and individually scaled to accommodate the full range of values for their "
                    "respective variables."
                ),
                dmc.Space(h="md"),
                dmc.Text(
                    "Data lines form the second essential component, where each individual observation or data record "
                    "appears as a polyline that traverses all the parallel axes. The position where each line intersects "
                    "an axis corresponds precisely to that data point's value for the variable represented by that axis. "
                    "These interconnected lines create a complex network that visually demonstrates how multiple variables "
                    "relate to one another across the entire dataset."
                ),
                dmc.Space(h="md"),
                dmc.Text("Reading the Chart", fw="bold"),
                dmc.Space(h="md"),
                dmc.Text(
                    "Parallel coordinates charts reveal multivariate patterns through the collective behavior of data "
                    "lines across all axes. Parallel lines indicate positive correlation between adjacent variables - "
                    "when lines maintain similar slopes between axes, it suggests the variables change together in the "
                    "same direction. Converging or diverging lines reveal negative correlations or inverse relationships "
                    "between variables."
                ),
                dmc.Space(h="md"),
                dmc.Text(
                    "Clustering becomes apparent when groups of lines follow similar paths across multiple axes, indicating "
                    "that certain observations share comparable characteristics across several dimensions. Outliers stand "
                    "out as individual lines that deviate significantly from the main bundle of data paths, making anomalous "
                    "observations immediately visible across multiple variables simultaneously. The ability to examine "
                    "relationships between any combination of variables by focusing on specific axis pairs makes parallel "
                    "coordinates particularly valuable for exploratory data analysis in high-dimensional datasets."
                ),
            ]
        )
    ],
    withBorder=True,
    shadow="md",
    radius="md",
    w=600,
    pt=0,
)


