import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, html, callback, register_page, dcc
from utils.utils import get_data_from_db, aggregate_scores
import plotly.express as px
import plotly.graph_objects as go
import itertools

from data.options import (
    attachment_style_options,
    demographics_options,
    demographics_values,
    attachment_style_labels_values,
    demographics_labels_values, 
)
from components.box_plot import BoxModal, BoxThumbnail
from components.histogram_modal import HistogramModal, HistogramThumbnail
from components.scatter_plot import ScatterModal, ScatterThumbnail
from components.spider_plot import SpiderModal, SpiderThumbnail
from components.pie_plot import PieModal, PieThumbnail
from components.parallel_plot import ParallelModal, ParallelThumbnail

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
                    html.Div(
                        dcc.Graph(
                            id="pie-thumbnail",
                            config={"staticPlot": True},
                            style={"cursor": "pointer"},
                        ),
                        id="pie-container",
                        className="thumbnail",
                    ),
                    html.Div(
                        dcc.Graph(
                            id="histogram-thumbnail",
                            config={"staticPlot": True},
                            style={"cursor": "pointer"},
                        ),
                        id="histogram-container",
                        className="thumbnail",
                    ),
                    html.Div(
                        dcc.Graph(
                            id="parallel-thumbnail",
                            config={"staticPlot": True},
                            style={"cursor": "pointer"},
                        ),
                        id="parallel-container",
                        className="thumbnail",
                    ),
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











# GLOBAL PIE CHART
# toggle pie modal
@callback(
    Output("pie-modal", "is_open"),
    [Input("pie-container", "n_clicks"), Input("close-pie", "n_clicks")],
    State("pie-modal", "is_open"),
)
def toggle_pie_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update pie thumbnail
@callback(
    Output("pie-thumbnail", "figure"),
    [
        Input("global-pie-chart-dropdown-attachment-style", "value"),
        Input("global-pie-chart-dropdown-demographic", "value"),
        Input("data-store", "data"),
        Input("window-width", "data"),
    ],
)
def update_global_pie_thumbnail(
    attachment_style: str,
    demographic: str,
    data,
    window_width,
) -> go.Figure:
    answers_df = pd.DataFrame(data)
    options: tuple[str, ...] = tuple(
        option for option in demographics_values[demographic]
    )
    values: tuple[float, ...] = tuple(
        answers_df[answers_df[demographic] == option][attachment_style].mean()
        for option in options
    )

    if window_width[0] > 500:
        fig = px.pie(
            values=values,
            names=options,
            title="Global Pie Chart",
            width=300,
            height=250,
            # template="plotly_dark",
        )
        fig.update_layout(
            title_x=0.5,
            title_y=0.98,
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
    else:
        fig = px.pie(
            values=values,
            names=options,
            title="Global Pie Chart",
            width=165,
            height=180,
            # template="plotly_dark",
        )
        fig.update_layout(
            title_font_size=15,
            title_x=0.5,
            title_y=0.95,
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
        fig.update_traces(textinfo="none")

    return fig


# update pie graph
@callback(
    Output("pie-graph", "figure"),
    [
        Input("global-pie-chart-dropdown-attachment-style", "value"),
        Input("global-pie-chart-dropdown-demographic", "value"),
        Input("data-store", "data"),
    ],
)
def update_global_pie_graph(attachment_style: str, demographic: str, data) -> go.Figure:
    answers_df = pd.DataFrame(data)
    options: tuple[str, ...] = tuple(
        option for option in demographics_values[demographic]
    )
    values: tuple[float, ...] = tuple(
        answers_df[answers_df[demographic] == option][attachment_style].mean()
        for option in options
    )

    fig = px.pie(
        values=values,
        names=options,
        title=f"{attachment_style.replace('_', ' ').capitalize()} distribution"
        f" by {demographic.replace('_', ' ')}",
        # template="plotly_dark",
    )

    return fig


# HISTOGRAM
# toggle histgram modal
@callback(
    Output("histogram-modal", "is_open"),
    [Input("histogram-container", "n_clicks"), Input("close-histogram", "n_clicks")],
    State("histogram-modal", "is_open"),
)
def toggle_histogram_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update histogram thumbnail
@callback(
    Output("histogram-thumbnail", "figure"),
    [
        Input("attachment-style-dropdown-histo", "value"),
        Input("data-store", "data"),
        Input("window-width", "data"),
    ],
)
def update_histo_thumbnail(selected_style, data, window_width):
    answers_df = pd.DataFrame(data)
    if window_width[0] > 500:
        fig = px.histogram(
            answers_df,
            x=selected_style,
            nbins=20,
            title="Histogram",
            width=300,
            height=250,
        )
        fig.update_layout(
            title_x=0.57,
            title_y=0.98,
            xaxis_title="",
            yaxis_title="",
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
    else:
        fig = px.histogram(
            answers_df,
            x=selected_style,
            nbins=20,
            title="Histogram",
            width=175,
            height=175,
        )
        fig.update_layout(
            title_font_size=15,
            title_x=0.59,
            title_y=0.95,
            xaxis_title="",
            yaxis_title="",
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
    return fig


# update histogram modal
@callback(
    Output("histogram-graph", "figure"),
    [Input("attachment-style-dropdown-histo", "value"), Input("data-store", "data")],
)
def update_histo_modal(selected_style, data):
    answers_df = pd.DataFrame(data)
    fig = px.histogram(
        answers_df,
        x=selected_style,
        nbins=20,
        title=f'Distribution of {selected_style.split("_")[0].capitalize()} '
        f'Attachment Scores',
    )
    fig.update_layout(
        xaxis_title=selected_style.split("_")[0].capitalize() + " Attachment Score",
        yaxis_title="Count",
    )
    return fig


# PARALLEL CATEGORIES
# toggle parallel modal
@callback(
    Output("parallel-modal", "is_open"),
    [Input("parallel-container", "n_clicks"), Input("close-parallel", "n_clicks")],
    State("parallel-modal", "is_open"),
)
def toggle_parallel_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update parallel thumbnail
@callback(
    Output("parallel-thumbnail", "figure"),
    [
        Input("parallel-categories-dropdown", "value"),
        Input("parallel-color-dropdown", "value"),
        Input("data-store", "data"),
        Input("window-width", "data"),
    ],
)
def update_parallel_thumnail(selected_dims, color_by, data, window_width):
    answers_df = pd.DataFrame(data)
    if not selected_dims:
        selected_dims = ["gender"]
    if window_width[0] > 500:
        if color_by == "any":
            fig = px.parallel_categories(
                answers_df,
                dimensions=selected_dims,
                color_continuous_scale=px.colors.sequential.Inferno,
                title="Parallel Categories Diagram",
            )
        else:
            fig = px.parallel_categories(
                answers_df,
                dimensions=selected_dims,
                color=color_by,
                color_continuous_scale=px.colors.sequential.Inferno,
                title="Parallel Categories Diagram",
                width=300,
                height=250,
            )
        fig.update_layout(
            title_x=0.5,
            title_y=0.98,
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
        fig.update_coloraxes(showscale=False)
        for dim in fig.data[0]["dimensions"]:
            dim["label"] = ""
    else:
        if color_by == "any":
            fig = px.parallel_categories(
                answers_df,
                dimensions=selected_dims,
                color_continuous_scale=px.colors.sequential.Inferno,
                title="Parallel Categories Diagram",
            )
        else:
            fig = px.parallel_categories(
                answers_df,
                dimensions=selected_dims,
                color=color_by,
                color_continuous_scale=px.colors.sequential.Inferno,
                title="Parallel Categories",
                width=175,
                height=175,
            )
        fig.update_layout(
            title_font_size=15,
            title_x=0.5,
            title_y=0.95,
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
        fig.update_coloraxes(showscale=False)
        for dim in fig.data[0]["dimensions"]:
            dim["label"] = ""
        fig.update_traces(
            {"tickfont": {"size": 1, "color": "white"}}
        )
    return fig


# update parallel graph
@callback(
    Output("parallel-graph", "figure"),
    [
        Input("parallel-categories-dropdown", "value"),
        Input("parallel-color-dropdown", "value"),
        Input("data-store", "data"),
    ],
)
def update_parallel_graph(selected_dims, color_by, data):
    answers_df = pd.DataFrame(data)
    if not selected_dims:
        selected_dims = ["gender"]
    if color_by == "any":
        fig = px.parallel_categories(
            answers_df,
            dimensions=selected_dims,
            color_continuous_scale=px.colors.sequential.Inferno,
            title="Parallel Categories Diagram",
        )
    else:
        fig = px.parallel_categories(
            answers_df,
            dimensions=selected_dims,
            color=color_by,
            color_continuous_scale=px.colors.sequential.Inferno,
            title="Parallel Categories Diagram",
        )
    return fig
