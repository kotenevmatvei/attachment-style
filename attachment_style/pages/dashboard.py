from dash import Input, Output, html, callback, register_page, dcc
from utils.utils import retrieve_scores_from_db
import plotly.graph_objects as go

from components.dashboard.box_plot import BoxModal, BoxThumbnail
from components.dashboard.histogram_plot import HistogramModal, HistogramThumbnail
from components.dashboard.scatter_plot import ScatterModal, ScatterThumbnail
from components.dashboard.spider_plot import SpiderModal, SpiderThumbnail
from components.dashboard.pie_plot import PieModal, PieThumbnail
from components.dashboard.parallel_plot import ParallelModal, ParallelThumbnail

register_page(__name__, path="/dashboard")

fig = go.Figure()
scores = retrieve_scores_from_db()


def layout(**kwargs):
    return html.Div(
        [
            html.H3("Dashboard", className="text-center mb-2"),
            dcc.Checklist(
                ["Include test data"],
                ["Include test data"],
                id="include_test_data",
            ),
            html.Div("Click on the thumbnails to explore the graphs", className="mb-4"),
            html.Div(
                children=[
                    BoxThumbnail,
                    ScatterThumbnail,
                    SpiderThumbnail,
                    PieThumbnail,
                    HistogramThumbnail,
                    ParallelThumbnail,
                ],
                className="thumbnail-container",
            ),
            BoxModal,
            HistogramModal,
            ScatterModal,
            SpiderModal,
            PieModal,
            ParallelModal,
            dcc.Store(id="data-store", data=scores),
        ]
    )


# switch between test and real data
@callback(
    Output("data-store", "data"),
    Input("include_test_data", "value"),
)
def include_test_data(include_test_data):
    scores = retrieve_scores_from_db()
    # todo add the option to keep both test and real data like in the initial load
    test = True if include_test_data == ["Include test data"] else False

    if test == True:
        return scores
    else:
        indices_to_keep = [
            i for i, test_val in enumerate(scores["test"]) if test_val == False
        ]
        filtered_scores = {
            key: [scores[key][i] for i in indices_to_keep] for key in scores.keys()
        }

        return filtered_scores
