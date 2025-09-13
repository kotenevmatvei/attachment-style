import logging

import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import register_page, dcc

import constants
from components.dashboard.box_plot import BoxCard
from components.dashboard.parallel_plot import ParallelCard
from components.dashboard.scatter_3d import Scatter3dCard
from components.dashboard.scatter_plot import ScatterCard
from components.dashboard.dashboard_settings import DashboardSettings
from components.dashboard.KPIs import DashboardKPIs
from utils.database import retrieve_scores_from_db

import constants

logger = logging.getLogger(__name__)

register_page(__name__, path="/dashboard")

fig = go.Figure()


def layout(**kwargs):
    return [
        DashboardSettings,
        DashboardKPIs,
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
    ]
