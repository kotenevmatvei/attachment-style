import logging

import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import register_page, callback, Input, Output

import constants
from components.dashboard.box_plot import BoxCard
from components.dashboard.parallel_plot import ParallelCard
from components.dashboard.scatter_3d import Scatter3dCard
from components.dashboard.scatter_plot import ScatterCard
from components.dashboard.dashboard_filters import DashboardFilters, DashboardFiltersMobile
from components.dashboard.KPIs import DashboardKPIs
from utils.database import retrieve_scores_from_db

import constants

logger = logging.getLogger(__name__)

register_page(__name__, path="/dashboard")



def layout(**kwargs):
    return [
        DashboardFilters,
        DashboardFiltersMobile,
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

@callback(
    [
        Output("box-plot-title", "order"),
        Output("scatter-plot-title", "order"),
        Output("scatter-3d-plot-title", "order"),
        Output("parallel-plot-title", "order"),

        Output("boxplot-card", "w"),
        Output("scatter-plot-card", "w"),
        Output("scatter3d-plot-card", "w"),
        Output("parallel-plot-card", "w"),

        Output("scatter-x-dropdown", "size"),
        Output("scatter-y-dropdown", "size"),

        Output("scatter-x-dropdown", "w"),
        Output("scatter-y-dropdown", "w"),

    ],
    Input("window-width", "data"),
)
def resize_feedback_page_title(window_width):
    if window_width < 500:
        return (
            4, 4, 4, 4,
            "95%", "95%", "95%", "95%",
            "sm", "sm",
            "45%", "45%",
        )
    return (
        2, 2, 2, 2,
        600,600,600,600,
        "md", "md",
        None, None
    )
