import dash_bootstrap_components as dbc
from dash import dcc

Dashboard = dbc.Card(
    children=[
        dcc.Markdown("Dashboard")
    ],
    className="mb-4 text-center border"
)
