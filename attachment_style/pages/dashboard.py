from dash import Input, Output, html, callback, register_page, dcc
from utils.utils import get_data_from_db, aggregate_scores
import plotly.graph_objects as go

from components.dashboard.box_plot import BoxModal, BoxThumbnail
from components.dashboard.histogram_plot import HistogramModal, HistogramThumbnail
from components.dashboard.scatter_plot import ScatterModal, ScatterThumbnail
from components.dashboard.spider_plot import SpiderModal, SpiderThumbnail
from components.dashboard.pie_plot import PieModal, PieThumbnail
from components.dashboard.parallel_plot import ParallelModal, ParallelThumbnail

register_page(__name__, path="/dashboard")


df1, df2 = get_data_from_db(test=True)
df1, df2 = aggregate_scores(df1, df2)
answers_df = df1

fig = go.Figure()



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
            dcc.Store(id="data-store", data={}),
        ]
    )


# load the data from db
@callback(
    Output("data-store", "data"),
    Input("include_test_data", "value"),
)
def include_test_data(include_test_data):
    if include_test_data == ["Include test data"]:
        df1, df2 = get_data_from_db(test=True)
        df1, df2 = aggregate_scores(df1, df2)
        answers_dict = df1.to_dict()
        return answers_dict
    df1, df2 = get_data_from_db(test=False)
    df1, df2 = aggregate_scores(df1, df2)
    answers_dict = df1.to_dict()
    return answers_dict














