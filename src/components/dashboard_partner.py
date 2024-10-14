import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

import plotly.express as px

DashboardPartner = dbc.Collapse(
    dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=px.pie([1, 2, 3]), id="pie-chart-partner")),
            dbc.Col(dcc.Markdown(id="type-description-markdown-partner")),
        ],
        className="d-flex align-items-center",
    ),
    # children=[
    #     dcc.Graph(figure=px.pie([1, 2, 3]), id="pie-chart-partner"),
    #     dcc.Markdown(id="type-description-markdown-partner")
    # ],
    id="dashboard-collapse-partner",
    is_open=False,
    className="mb-4 text-center",
)
