import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, callback, register_page, dcc
from attachment_style.utils.utils import get_data_from_db, aggregate_scores
import plotly.express as px
import pandas as pd

register_page(__name__, path="/dashboard_modal")


df1, df2 = get_data_from_db(test=True)
df1, df2 = aggregate_scores(df1, df2)
answers_df = df1
attachment_styles = ["avoidant_score", "secure_score", "anxious_score"]

distro = html.Div(
    [
        html.Label("Select Attachment Style:"),
        dcc.Dropdown(
            id="attachment-style-dropdown",
            options=[
                {
                    "label": style.split("_")[0].capitalize(),
                    "value": style,
                }
                for style in attachment_styles
            ],
            value="avoidant_score",
        ),
        dcc.Graph(id="distribution-histogram-modal"),
    ]
)

scatter = html.Div(
    [
        html.Label("Select X-axis Variable:"),
        dcc.Dropdown(
            id="scatter-x-dropdown",
            options=[
                {"label": "Age", "value": "age"},
                {
                    "label": "Avoidant Score",
                    "value": "avoidant_score",
                },
                {
                    "label": "Secure Score",
                    "value": "secure_score",
                },
                {
                    "label": "Anxious Score",
                    "value": "anxious_score",
                },
            ],
            value="age",
        ),
        html.Label("Select Y-axis Variable:"),
        dcc.Dropdown(
            id="scatter-y-dropdown",
            options=[
                {
                    "label": "Avoidant Score",
                    "value": "avoidant_score",
                },
                {
                    "label": "Secure Score",
                    "value": "secure_score",
                },
                {
                    "label": "Anxious Score",
                    "value": "anxious_score",
                },
            ],
            value="avoidant_score",
        ),
        html.Label("Color By:"),
        dcc.Dropdown(
            id="scatter-color-dropdown",
            options=[
                {"label": "None", "value": "None"},
                {"label": "Gender", "value": "gender"},
                {
                    "label": "Therapy Experience",
                    "value": "therapy_experience",
                },
                {
                    "label": "Relationship Status",
                    "value": "relationship_status",
                },
            ],
            value="gender",
        ),
        dcc.Graph(id="scatter-plot"),
    ]
)


def layout(**kwargs):
    return html.Div(
        [
            dbc.Row(
                children=[
                    dbc.Col(
                        dbc.Container(
                            html.Div(
                                [
                                    html.Div(
                                        dcc.Graph(
                                            id="distribution-histogram-thumbnail",
                                            config={"staticPlot": True},
                                            style={"cursor": "pointer"},
                                        ),
                                        id="histogram-container",
                                    ),
                                ],
                            ),
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Container(
                            html.Div(
                                [
                                    html.Div(
                                        dcc.Graph(
                                            id="scatter-thumbnail",
                                            config={"staticPlot": True},
                                            style={"cursor": "pointer"},
                                        ),
                                        id="scatter-container",
                                    ),
                                ],
                            ),
                        ),
                        width=4,
                    ),
                ]
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Header")),
                    dbc.ModalBody(distro),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="close-histogram",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="modal-histogram",
                is_open=False,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Header")),
                    dbc.ModalBody(distro),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close-scatter", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal-scatter",
                is_open=False,
            ),
        ]
    )


@callback(
    Output("modal-histogram", "is_open"),
    [Input("histogram-container", "n_clicks"), Input("close-histogram", "n_clicks")],
    [State("modal-histogram", "is_open")],
)
def toggle_histogram_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@callback(
    Output("modal-scatter", "is_open"),
    [Input("scatter-container", "n_clicks"), Input("close-scatter", "n_clicks")],
    [State("modal-scatter", "is_open")],
)
def toggle_scatter_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Callbacks for interactivity
@callback(
    Output("distribution-histogram-thumbnail", "figure"),
    [
        Input("attachment-style-dropdown", "value"),
        # Input("data_store", "data"),
    ],
)
def update_distribution_thumbnail(selected_style):  # , data):
    # answers_df = pd.DataFrame(data)
    fig = px.histogram(  # type: ignore
        answers_df,
        x=selected_style,
        nbins=20,
        title="Histogram",
        width=400,
        height=300,
    )
    fig.update_xaxes(
        title=selected_style.split("_")[0].capitalize() + " Attachment Score"
    )
    fig.update_yaxes(title="Count")
    return fig


# Callbacks for interactivity
@callback(
    Output("distribution-histogram-modal", "figure"),
    [
        Input("attachment-style-dropdown", "value"),
        # Input("data_store", "data"),
    ],
)
def update_distribution_modal(selected_style):  # , data):
    # answers_df = pd.DataFrame(data)
    fig = px.histogram(  # type: ignore
        answers_df,
        x=selected_style,
        nbins=20,
        title=f'Distribution of {selected_style.split("_")[0].capitalize()} Attachment Scores',
    )
    fig.update_xaxes(
        title=selected_style.split("_")[0].capitalize() + " Attachment Score"
    )
    fig.update_yaxes(title="Count")
    return fig


@callback(
    Output("scatter-thumbnail", "figure"),
    [
        Input("scatter-x-dropdown", "value"),
        Input("scatter-y-dropdown", "value"),
        Input("scatter-color-dropdown", "value"),
    ],
)
def update_scatter_thumbnail(x_var, y_var, color_var, data):
    answers_df = pd.DataFrame(data)
    if color_var == "None":
        fig = px.scatter(
            answers_df,
            x=x_var,
            y=y_var,
            title=f'{y_var.split("_")[0].capitalize()} vs {x_var.capitalize()}',
        )
    else:
        fig = px.scatter(
            answers_df,
            x=x_var,
            y=y_var,
            color=color_var,
        )
    fig.update_xaxes(title=x_var.replace("_", " ").title())
    fig.update_yaxes(title=y_var.replace("_", " ").title())
    return fig

@callback(
    Output("modal-scatter", "figure"),
    [
        Input("scatter-x-dropdown", "value"),
        Input("scatter-y-dropdown", "value"),
        Input("scatter-color-dropdown", "value"),
    ],
)
def update_scatter_modal(x_var, y_var, color_var, data):
    answers_df = pd.DataFrame(data)
    if color_var == "None":
        fig = px.scatter(
            answers_df,
            x=x_var,
            y=y_var,
            title=f'{y_var.split("_")[0].capitalize()} vs {x_var.capitalize()}',
        )
    else:
        fig = px.scatter(
            answers_df,
            x=x_var,
            y=y_var,
            color=color_var,
            title=f'{y_var.split("_")[0].capitalize()} vs {x_var.capitalize()} Colored by {color_var.replace("_", " ").title()}',
        )
    fig.update_xaxes(title=x_var.replace("_", " ").title())
    fig.update_yaxes(title=y_var.replace("_", " ").title())
    return fig
