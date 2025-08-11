from dash import Input, Output, html, callback, register_page, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from utils.utils import retrieve_scores_from_db
import plotly.graph_objects as go
import logging

from components.simple_dashboard.box_plot import BoxCard
from components.simple_dashboard.scatter_plot import ScatterCard
from components.simple_dashboard.parallel_plot import ParallelCard
from components.simple_dashboard.scatter_3d import Scatter3dCard

logger = logging.getLogger(__name__)

register_page(__name__, path="/simple_dashboard")

fig = go.Figure()
scores = retrieve_scores_from_db()
logger.info("Retrieved scores from the db for the first time")


def layout(**kwargs):
    return dmc.MantineProvider(
        children=[
            dmc.Flex(
                gap="md",
                justify="center",
                align="center",
                direction="row",
                wrap="wrap",
                mt="xl",
                mb="xl",
                children=[
                    dmc.Badge("Total submissions: 124", size="xl", p="lg"),
                    dmc.Badge("Most common style: Anxious", size="xl", p="lg"),
                    dmc.Badge("Avg anxious score: 2.5", size="xl", p="lg"),
                    dmc.Badge("Avg avoidant score: 2.5", size="xl", p="lg"),
                    dmc.Badge("Avg secure score: 2.5", size="xl", p="lg"),
                ],
            ),
            dmc.Flex(
                gap="md",
                justify="center",
                align="center",
                direction="row",
                wrap="wrap",
                mb="md",
                children=[
                    dmc.Button("Refresh data", size="md", mr="xs"),
                    dmc.Text("Select the dataset:", size="lg"),
                    dmc.MultiSelect(
                        # label="Select the dataset:",
                        data=[
                            {"label": "Assess Yourself", "value": "assess_yourself"},
                            {"label": "Assess Others", "value": "assess_others"},
                        ],
                        value=["assess_yourself", "assess_others"],
                        size="lg",
                        comboboxProps={"shadow": "lg"},
                    ),
                    dmc.Checkbox("Include test data", size="lg", mr="xs"),
                ],
            ),
            dmc.Flex(
                gap="md",
                justify="center",
                direction="row",
                wrap="wrap",
                children=[
                    BoxCard,
                    ScatterCard,
                    Scatter3dCard,
                    ParallelCard,
                ],
            ),
            dcc.Store("data-store", data=scores),
        ]
    )
