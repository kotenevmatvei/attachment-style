import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html
from dash import dcc

Dashboard = html.Div(
    children=[
        dcc.Graph(figure=px.pie([1, 2, 3]), id="pie-chart")
    ],
    id="dashboard-div",
    hidden=True,
    className="mb-4 text-center border"
)
