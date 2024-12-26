import dash_bootstrap_components as dbc
from dash import dcc

import plotly.express as px

ChartOthers = dbc.Collapse(
    dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=px.pie([1, 2, 3]), id="pie-chart-partner")),
            dbc.Col(dcc.Markdown(id="type-description-markdown-partner")),
        ],
        className="d-flex align-items-center",
    ),
    id="dashboard-collapse-partner",
    is_open=False,
    className="mb-4 text-center",
)
