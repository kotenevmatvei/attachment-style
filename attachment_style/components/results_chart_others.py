import dash_bootstrap_components as dbc
from dash import dcc, html

import plotly.express as px

ResultChartOthers = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Your Results")),
        dbc.ModalBody(
            [
                dcc.Graph(figure=px.pie([1, 2, 3]), id="pie-chart-others"),
                dcc.Markdown(id="type-description-markdown-others"),
            ],
        ),
        dbc.ModalFooter(
            [
                html.Div(
                    "Here you can download your full report with all questions and answers:",
                    style={"color": "#CB997E", "margin-right":10},
                ),
                dbc.Button("PDF", id="download-report-button-others"),
            ],
            id="download-report-collapse-others",
            className="d-flex",
        ),
    ],
    id="dashboard-collapse-others",
    is_open=False,
    size="lg",
)
