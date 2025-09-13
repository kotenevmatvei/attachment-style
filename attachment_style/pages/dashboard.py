import logging

import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import register_page, dcc
from dash_iconify import DashIconify

import constants
from components.dashboard.box_plot import BoxCard
from components.dashboard.parallel_plot import ParallelCard
from components.dashboard.scatter_3d import Scatter3dCard
from components.dashboard.scatter_plot import ScatterCard
from utils.database import retrieve_scores_from_db

import constants

logger = logging.getLogger(__name__)

register_page(__name__, path="/dashboard")

fig = go.Figure()
scores = retrieve_scores_from_db()
logger.info("Retrieved scores from the db for the first time")


def layout(**kwargs):
    return [
        dmc.Flex(
            gap="md",
            justify="center",
            align="center",
            direction="row",
            wrap="wrap",
            mb="md",
            children=[
                dmc.Button(
                    "Refresh Data",
                    leftSection=DashIconify(
                        icon="tabler:refresh", width=16
                    ),
                    variant="light",
                ),
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
                dmc.Switch("Include test data", size="lg", mr="xs"),
            ],
        ),
        dmc.Paper(
            [
                # Statistics in a grid instead of badges
                dmc.SimpleGrid(
                    cols=4,
                    children=[
                        dmc.Paper(
                            [
                                dmc.Stack(
                                    [
                                        dmc.Text(
                                            "Anxious: 57%",
                                            size="xl",
                                            fw=700,
                                            ta="center",
                                            c=constants.PRIMARY,
                                        ),
                                        dmc.Text(
                                            "Dominant attachment style",
                                            size="sm",
                                            c="dimmed",
                                            ta="center",
                                        ),
                                    ],
                                    gap=0,
                                ),
                            ],
                            p="md",
                            radius="md",
                            withBorder=True,
                        ),
                        dmc.Paper(
                            [
                                dmc.Stack(
                                    [
                                        dmc.Text(
                                            "Female: 48%",
                                            size="xl",
                                            fw=700,
                                            ta="center",
                                            c=constants.PRIMARY,
                                        ),
                                        dmc.Text(
                                            "Dominant gender",
                                            size="sm",
                                            c="dimmed",
                                            ta="center",
                                        ),
                                    ],
                                    gap=0,
                                ),
                            ],
                            p="md",
                            radius="md",
                            withBorder=True,
                        ),
                        dmc.Paper(
                            [
                                dmc.Stack(
                                    [
                                        dmc.Text(
                                            "Some: 49%",
                                            size="xl",
                                            fw=700,
                                            ta="center",
                                            c=constants.PRIMARY,
                                        ),
                                        dmc.Text(
                                            "Dominant therapy experience",
                                            size="sm",
                                            c="dimmed",
                                            ta="center",
                                        ),
                                    ],
                                    gap=0,
                                ),
                            ],
                            p="md",
                            radius="md",
                            withBorder=True,
                        ),
                        dmc.Paper(
                            [
                                dmc.Stack(
                                    [
                                        dmc.Text(
                                            "124",
                                            size="xl",
                                            fw=700,
                                            ta="center",
                                            c=constants.PRIMARY,
                                        ),
                                        dmc.Text(
                                            "Total Submissions",
                                            size="sm",
                                            c="dimmed",
                                            ta="center",
                                        ),
                                    ],
                                    gap=0,
                                ),
                            ],
                            p="md",
                            radius="md",
                            withBorder=True,
                        ),
                    ],
                    spacing="md",
                ),
            ],
            p="lg",
            radius="md",
            shadow="sm",
            mb="xl",
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
