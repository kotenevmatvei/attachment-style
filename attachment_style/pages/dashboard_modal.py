import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, callback, register_page, dcc
from attachment_style.utils.utils import get_data_from_db, aggregate_scores
import plotly.express as px
import plotly.graph_objects as go


register_page(__name__, path="/dashboard_modal")


df1, df2 = get_data_from_db(test=True)
df1, df2 = aggregate_scores(df1, df2)
answers_df = df1
attachment_styles = ["avoidant_score", "secure_score", "anxious_score"]


def layout(**kwargs):
    return html.Div(
        [
            html.Center(html.H3("Dashboard")),
            dbc.Row(
                children=[
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id="histogram-thumbnail",
                                config={"staticPlot": True},
                                style={"cursor": "pointer"},
                            ),
                            id="histogram-container",
                        ),
                        width=4,
                    ),
                ]
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Histogram")),
                    dbc.ModalBody(
                        html.Div(
                            [
                                html.Label("Select Attachment Style:"),
                                dcc.Dropdown(
                                    id="attachment-style-dropdown-histo",
                                    options=[
                                        {
                                            "label": style.split("_")[0].capitalize(),
                                            "value": style,
                                        }
                                        for style in attachment_styles
                                    ],
                                    value="avoidant_score",
                                ),
                                dcc.Graph(id="histogram-graph"),
                            ]
                        )
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="close-histogram",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="histogram-modal",
                is_open=False,
            ),
        ]
    )


# TOGGLE THE MODALS
@callback(
    Output("histogram-modal", "is_open"),
    [Input("histogram-container", "n_clicks"), Input("close-histogram", "n_clicks")],
    State("histogram-modal", "is_open"),
)
def toggle_histogram_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# UPDATE THUMBNAILS
@callback(
    Output("histogram-thumbnail", "figure"),
    Input("attachment-style-dropdown-histo", "value"),
)
def update_distribution_thumbnail(selected_style):
    fig = px.histogram(
        answers_df,
        x=selected_style,
        nbins=20,
        title="Histogram",
        width=400,
        height=250,
    )
    fig.update_layout(
        title_x=0.5,
        title_y=1,
        xaxis_title=selected_style.split("_")[0].capitalize() + " Attachment Score",
        yaxis_title="Count",
        margin=dict(t=30),
    )
    return fig


# UPDATE MODALS
@callback(
    Output("histogram-graph", "figure"),
    Input("attachment-style-dropdown-histo", "value"),
)
def update_distribution_modal(selected_style):
    fig = px.histogram(
        answers_df,
        x=selected_style,
        nbins=20,
        title=f'Distribution of {selected_style.split("_")[0].capitalize()} Attachment Scores',
    )
    fig.update_layout(
        xaxis_title=selected_style.split("_")[0].capitalize() + " Attachment Score",
        yaxis_title="Count",
    )
    return fig
