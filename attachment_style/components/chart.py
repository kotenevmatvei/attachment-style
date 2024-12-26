import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html

Chart = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Your Results")),
        dbc.ModalBody(
            [
                dcc.Graph(figure=px.pie([1, 2, 3]), id="pie-chart"),
                dcc.Markdown(id="type-description-markdown"),
            ],
            # className="d-flex align-items-center",
        ),
        dbc.ModalFooter(
            [
                html.Div(
                    "Here you can download your full report with all questions and answers:",
                    style={"color": "purple", "margin-right":10},
                ),
                dbc.Button("PDF", id="download-report-button"),
            ],
            id="download-report-collapse",
            className="d-flex",
        ),
    ],
    # dbc.Row(
    #     [
    #         dbc.Col(dcc.Graph(figure=px.pie([1, 2, 3]), id="pie-chart")),
    #         dbc.Col(dcc.Markdown(id="type-description-markdown")),
    #     ],
    #     className="d-flex align-items-center",
    # ),
    id="dashboard-collapse",
    is_open=False,
    size="lg",
    # className="mb-4 text-center",
)
