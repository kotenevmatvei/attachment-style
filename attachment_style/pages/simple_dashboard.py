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
                # cols=2,
                # spacing="sm",
                # verticalSpacing="sm",
                gap="md",
                justify="center",
                direction="row",
                wrap="wrap",
                children=[
                    BoxCard,
                    ScatterCard,
                    Scatter3dCard,
                    ParallelCard,
                ]
            ),
            dcc.Store("data-store", data=scores)
        ]
    )


