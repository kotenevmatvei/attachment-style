import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc

Dashboard = dbc.Collapse(
    dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=px.pie([1, 2, 3]), id="pie-chart")),
            dbc.Col(dcc.Markdown(id="type-description-markdown")),
        ],
        className="d-flex align-items-center",
    ),
    id="dashboard-collapse",
    is_open=False,
    className="mb-4 text-center",
)
