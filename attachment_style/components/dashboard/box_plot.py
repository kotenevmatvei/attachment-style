from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from data.options import demographics_labels_values, attachment_style_labels_values
import pandas as pd
import plotly.express as px

BoxThumbnail = html.Div(
    dcc.Graph(
        id="box-thumbnail",
        config={"staticPlot": True},
        style={"cursor": "pointer"},
    ),
    id="box-container",
    className="thumbnail",
)

BoxModal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Box Plot")),
        dbc.ModalBody(
            [
                html.Label("Select Demographic Variable:"),
                dcc.RadioItems(
                    id="demographic-radio",
                    options=demographics_labels_values,
                    value="gender",
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "10px",
                    },
                    className="mb-2",
                ),
                html.Label("Select Attachment Style:"),
                dcc.Dropdown(
                    id="attachment-style-dropdown-demographics",
                    options=attachment_style_labels_values,
                    value="avoidant_score",
                ),
                dcc.Graph(id="box-graph"),
            ]
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Close",
                id="close-box",
                className="ms-auto",
                n_clicks=0,
            )
        ),
    ],
    id="box-modal",
    size="lg",
    is_open=False,
)


# toggle modal
@callback(
    Output("box-modal", "is_open"),
    [Input("box-container", "n_clicks"), Input("close-box", "n_clicks")],
    State("box-modal", "is_open"),
)
def toggle_box_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update box plot graph
@callback(
    Output("box-graph", "figure"),
    [
        Input("demographic-radio", "value"),
        Input("attachment-style-dropdown-demographics", "value"),
        Input("data-store", "data"),
    ],
)
def update_box_graph(demographic, selected_style, data):
    answers_df = pd.DataFrame(data)
    fig = px.box(
        answers_df,
        x=demographic,
        y=selected_style,
        title=f'{selected_style.split("_")[0].capitalize()} '
        f'Attachment Scores by {demographic.replace("_", " ").title()}',
    )
    fig.update_xaxes(title=demographic.replace("_", " ").title())
    fig.update_yaxes(
        title=selected_style.split("_")[0].capitalize() + " Attachment Score"
    )
    return fig


# update box plot thumbnail
@callback(
    Output("box-thumbnail", "figure"),
    [
        Input("demographic-radio", "value"),
        Input("attachment-style-dropdown-demographics", "value"),
        Input("data-store", "data"),
        Input("window-width", "data"),
    ],
)
def update_box_thumbnail(demographic, selected_style, data, window_width):
    answers_df = pd.DataFrame(data)
    if window_width[0] > 500:
        fig = px.box(
            answers_df,
            x=demographic,
            y=selected_style,
            title="Box Plot",
            width=300,
            height=250,
        )
        fig.update_layout(
            title_x=0.5,
            title_y=0.98,
            xaxis_title="",
            yaxis_title="",
            margin=dict(t=30, r=0, l=0),
            showlegend=False,
        )
    else:
        fig = px.box(
            answers_df,
            x=demographic,
            y=selected_style,
            title="Box Plot",
            width=175,
            height=175,
        )
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        (
            fig.update_layout(
                title_font_size=15,
                title_x=0.57,
                title_y=0.95,
                xaxis_title="",
                yaxis_title="",
                margin=dict(t=30, r=0, l=0),
                showlegend=False,
            ),
        )
    return fig
