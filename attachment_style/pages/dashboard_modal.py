from os import X_OK
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, html, callback, register_page, dcc
from attachment_style.utils.utils import get_data_from_db, aggregate_scores
import plotly.express as px
import plotly.graph_objects as go
import itertools


register_page(__name__, path="/dashboard_modal")


df1, df2 = get_data_from_db(test=True)
df1, df2 = aggregate_scores(df1, df2)
answers_df = df1

attachment_style_options: dict[str, str] = {
    "Avoidant Score": "avoidant_score",
    "Secure Score": "secure_score",
    "Anxious Score": "anxious_score",
}

demographics_options: dict[str, str] = {
    "Gender": "gender",
    "Therapy Experience": "therapy_experience",
    "Relationship Status": "relationship_status",
}

demographics_values: dict[str, tuple[str, ...]] = {
    "gender": ("male", "female", "other"),
    "therapy_experience": ("extensive", "some", "none"),
    "relationship_status": ("married", "in_relationship", "single"),
}


def layout(**kwargs):
    return html.Div(
        [
            html.H3("Dashboard", className="text-center mb-2"),
            dcc.Checklist(
                ["Include test data"],
                ["Include test data"],
                id="include_test_data",
                className="mb-2",
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id="box-thumbnail",
                                config={"staticPlot": True},
                                style={"cursor": "pointer"},
                            ),
                            id="box-container",
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id="scatter-thumbnail",
                                config={"staticPlot": True},
                                style={"cursor": "pointer"},
                            ),
                            id="scatter-container",
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id="spider-thumbnail",
                                config={"staticPlot": True},
                                style={"cursor": "pointer"},
                            ),
                            id="spider-container",
                        ),
                        width=4,
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id="pie-thumbnail",
                                config={"staticPlot": True},
                                style={"cursor": "pointer"},
                            ),
                            id="pie-container",
                        ),
                        width=4,
                    ),
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
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id="parallel-thumbnail",
                                config={"staticPlot": True},
                                style={"cursor": "pointer"},
                            ),
                            id="parallel-container",
                        ),
                        width=4,
                    ),
                ],
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Box Plot")),
                    dbc.ModalBody(
                        [
                            html.Label("Select Demographic Variable:"),
                            dcc.RadioItems(
                                id="demographic-radio",
                                options=[
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
                                labelStyle={
                                    "display": "inline-block",
                                    "margin-right": "10px",
                                },
                                className="mb-2",
                            ),
                            html.Label("Select Attachment Style:"),
                            dcc.Dropdown(
                                id="attachment-style-dropdown-demographics",
                                options=[
                                    {
                                        "label": style.split("_")[0].capitalize(),
                                        "value": style,
                                    }
                                    for style in attachment_style_options.values()
                                ],
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
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Histogram")),
                    dbc.ModalBody(
                        [
                            html.Label("Select Attachment Style:"),
                            dcc.Dropdown(
                                id="attachment-style-dropdown-histo",
                                options=[
                                    {
                                        "label": style.split("_")[0].capitalize(),
                                        "value": style,
                                    }
                                    for style in attachment_style_options.values()
                                ],
                                value="avoidant_score",
                            ),
                            dcc.Graph(id="histogram-graph"),
                        ]
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
                size="lg",
                is_open=False,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Scatter Plot")),
                    dbc.ModalBody(
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
                            html.Div(
                                "Please choose the Y variable different from X",
                                id="scatter-y-warning",
                                style={"color": "red"},
                                hidden=True,
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
                            dcc.Graph(id="scatter-graph"),
                        ]
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="close-scatter",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="scatter-modal",
                size="lg",
                is_open=False,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Spider Chart")),
                    dbc.ModalBody(
                        [
                            html.Label("Select the attachment style:"),
                            dcc.Dropdown(
                                id="spider-attachment-style-dropdown",
                                options=[
                                    {
                                        "label": "Anxious",
                                        "value": "anxious_score",
                                    },
                                    {
                                        "label": "Secure",
                                        "value": "secure_score",
                                    },
                                    {
                                        "label": "Avoidant",
                                        "value": "avoidant_score",
                                    },
                                ],
                                clearable=False,
                                value="anxious_score",
                            ),
                            html.Label(
                                "Select Demographic Grouping for the shape "
                                "(at least one):"
                            ),
                            dcc.Dropdown(
                                id="spider-shape-dropdown",
                                options=[
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
                                value=["gender", "relationship_status"],
                                clearable=False,
                                multi=True,
                            ),
                            html.Label("Select Demographic Grouping for the color:"),
                            dcc.Dropdown(
                                id="spider-color-dropdown",
                                options=[
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
                                value=["therapy_experience"],
                                multi=True,
                            ),
                            dcc.Graph(id="spider-chart"),
                        ]
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="close-spider",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="spider-modal",
                size="lg",
                is_open=False,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Global Pie Chart")),
                    dbc.ModalBody(
                        [
                            html.Label("Select the attachment style"),
                            dcc.Dropdown(
                                id="global-pie-chart-dropdown-attachment-style",
                                options=[
                                    {
                                        "label": "Anxious",
                                        "value": "anxious_score",
                                    },
                                    {
                                        "label": "Secure",
                                        "value": "secure_score",
                                    },
                                    {
                                        "label": "Avoidant",
                                        "value": "avoidant_score",
                                    },
                                ],
                                value="anxious_score",
                            ),
                            html.Label("Select the demographic"),
                            dcc.Dropdown(
                                id="global-pie-chart-dropdown-demographic",
                                options=[
                                    {
                                        "label": "Gender",
                                        "value": "gender",
                                    },
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
                            dcc.Graph(id="pie-graph"),
                        ]
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="close-pie",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="pie-modal",
                size="lg",
                is_open=False,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Parallel Categories Plot")),
                    dbc.ModalBody(
                        [
                            html.Label("Select Variables:"),
                            dcc.Dropdown(
                                id="parallel-categories-dropdown",
                                options=[
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
                                value=["gender", "therapy_experience"],
                                multi=True,
                            ),
                            html.Label("Color By Attachment Style:"),
                            dcc.Dropdown(
                                id="parallel-color-dropdown",
                                options=[
                                    {
                                        "label": style.split("_")[0].capitalize(),
                                        "value": style,
                                    }
                                    for style in attachment_style_options.values()
                                ] + [{"label": "Any", "value": "any"}],
                                value="secure_score",
                            ),
                            dcc.Graph(id="parallel-graph"),
                        ]
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="close-parallel",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="parallel-modal",
                size="lg",
                is_open=False,
            ),
            dcc.Store(id="data-store", data={}),
        ]
    )


# load the data from db
@callback(
    Output("data-store", "data"),
    Input("include_test_data", "value"),
)
def include_test_data(include_test_data):
    if include_test_data == ["Include test data"]:
        df1, df2 = get_data_from_db(test=True)
        df1, df2 = aggregate_scores(df1, df2)
        answers_dict = df1.to_dict()
        return answers_dict
    df1, df2 = get_data_from_db(test=False)
    df1, df2 = aggregate_scores(df1, df2)
    answers_dict = df1.to_dict()
    return answers_dict


# BOX PLOT
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


# update box plot thumbnail
@callback(
    Output("box-thumbnail", "figure"),
    [
        Input("demographic-radio", "value"),
        Input("attachment-style-dropdown-demographics", "value"),
        Input("data-store", "data"),
    ],
)
def update_box_thumbnail(demographic, selected_style, data):
    answers_df = pd.DataFrame(data)
    fig = px.box(
        answers_df,
        x=demographic,
        y=selected_style,
        title="Box Plot",
        width=350,
        height=250,
    )
    fig.update_layout(
        title_x=0.5,
        title_y=0.98,
        xaxis_title="",
        yaxis_title="",
        margin=dict(t=30, r=15, l=15),
        showlegend=False,
    )
    return fig


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
        title=f'{selected_style.split("_")[0].capitalize()}'
        f'Attachment Scores by {demographic.replace("_", " ").title()}',
    )
    fig.update_xaxes(title=demographic.replace("_", " ").title())
    fig.update_yaxes(
        title=selected_style.split("_")[0].capitalize() + " Attachment Score"
    )
    return fig


# HISTOGRAM
# toggle histgram modal
@callback(
    Output("histogram-modal", "is_open"),
    [Input("histogram-container", "n_clicks"), Input("close-histogram", "n_clicks")],
    State("histogram-modal", "is_open"),
)
def toggle_histogram_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update histogram thumbnail
@callback(
    Output("histogram-thumbnail", "figure"),
    [
        Input("attachment-style-dropdown-histo", "value"),
        Input("data-store", "data"),
    ],
)
def update_histo_thumbnail(selected_style, data):
    answers_df = pd.DataFrame(data)
    fig = px.histogram(
        answers_df,
        x=selected_style,
        nbins=20,
        title="Histogram",
        width=350,
        height=250,
    )
    fig.update_layout(
        title_x=0.5,
        title_y=0.98,
        xaxis_title="",
        yaxis_title="",
        margin=dict(t=30, r=15, l=15),
        showlegend=False,
    )
    return fig


# update histogram modal
@callback(
    Output("histogram-graph", "figure"),
    [Input("attachment-style-dropdown-histo", "value"), Input("data-store", "data")],
)
def update_histo_modal(selected_style, data):
    answers_df = pd.DataFrame(data)
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


# SCATTER
# toggle modal
@callback(
    Output("scatter-modal", "is_open"),
    [Input("scatter-container", "n_clicks"), Input("close-scatter", "n_clicks")],
    State("scatter-modal", "is_open"),
)
def toggle_scatter_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update scatter thumbnail
@callback(
    Output("scatter-thumbnail", "figure"),
    [
        Input("scatter-x-dropdown", "value"),
        Input("scatter-y-dropdown", "value"),
        Input("scatter-color-dropdown", "value"),
        Input("data-store", "data"),
    ],
)
def update_scatter_thumbnail(x_var, y_var, color_var, data):
    answers_df = pd.DataFrame(data)
    if color_var == "None":
        fig = px.scatter(
            answers_df,
            x=x_var,
            y=y_var,
            title="Scatter Plot by Demographics",
            width=350,
            height=250,
        )
    else:
        fig = px.scatter(
            answers_df,
            x=x_var,
            y=y_var,
            color=color_var,
            title="Scatter Plot by Demographics",
            width=400,
            height=250,
        )
    fig.update_layout(
        title_x=0.5,
        title_y=0.98,
        xaxis_title="",
        yaxis_title="",
        margin=dict(t=30, r=15, l=15),
        showlegend=False,
    )
    return fig


# don't let the mdummies choose the same attachment style for x and y axes
@callback(Output("scatter-y-dropdown", "options"), Input("scatter-x-dropdown", "value"))
def update_scatter_y_options(x_value):
    not_used_options = [
        {"label": key, "value": val}
        for key, val in attachment_style_options.items()
        if val != x_value
    ]
    return not_used_options


# update scatter graph
@callback(
    [Output("scatter-graph", "figure"), Output("scatter-y-warning", "hidden")],
    [
        Input("scatter-x-dropdown", "value"),
        Input("scatter-y-dropdown", "value"),
        Input("scatter-color-dropdown", "value"),
        Input("data-store", "data"),
    ],
)
def update_scatter_graph(x_var, y_var, color_var, data):
    answers_df = pd.DataFrame(data)
    if y_var is None:
        return px.scatter([]), False
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
            title=f'{y_var.split("_")[0].capitalize()} vs {x_var.capitalize()} Colored '
            f'by {color_var.replace("_", " ").title()}',
        )
    fig.update_xaxes(title=x_var.replace("_", " ").title())
    fig.update_yaxes(title=y_var.replace("_", " ").title())
    return fig, True


# SPIDER CHART
# toggle spider modal
@callback(
    Output("spider-modal", "is_open"),
    [Input("spider-container", "n_clicks"), Input("close-spider", "n_clicks")],
    State("spider-modal", "is_open"),
)
def toggle_spider_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# only suggest by-color demographic options that have not already been chosen for shape.
@callback(
    Output("spider-color-dropdown", "options"),
    Input("spider-shape-dropdown", "value"),
)
def update_spider_color_options(used_shape_options: list[str]) -> list[dict[str, str]]:
    not_used_options = [
        {"label": key, "value": val}
        for key, val in demographics_options.items()
        if val not in used_shape_options
    ]
    return not_used_options


# spider thumbnail
@callback(
    Output("spider-thumbnail", "figure"),
    [
        Input("spider-attachment-style-dropdown", "value"),
        Input("spider-shape-dropdown", "value"),
        Input("spider-color-dropdown", "value"),
        Input("data-store", "data"),
    ],
)
def update_spider_thumbnail(
    attachment_style: str,
    demographics_shape: list[str],
    demographics_color: list[str],
    data,
) -> go.Figure:
    answers_df = pd.DataFrame(data)
    # if no options are chosen return empty figure
    if not demographics_shape:
        return px.line_polar()

    # for the chosen demographics get the tuples with corresponding values
    shape_options: tuple[tuple[str, ...], ...] = tuple(
        demographics_values[demographic] for demographic in demographics_shape
    )
    color_options: tuple[tuple[str, ...], ...] = tuple(
        demographics_values[demographic] for demographic in demographics_color
    )

    # create cartesian products representing all possible combinations
    color_combos: tuple[tuple[str, ...], ...] = tuple(itertools.product(*color_options))
    shape_combos: tuple[tuple[str, ...], ...] = tuple(itertools.product(*shape_options))

    # construct the queries
    if not demographics_color:  # without color
        queries: tuple[str, ...] = tuple(
            " & ".join(
                f"{k} == {repr(v)}" for k, v in zip(demographics_shape, shape_combo)
            )
            for shape_combo in shape_combos
        )
    else:  # with color
        color_queries: tuple[str, ...] = tuple(
            " & ".join(
                f"{k} == {repr(v)}" for k, v in zip(demographics_color, color_combo)
            )
            for color_combo in color_combos
        )
        queries: tuple[str, ...] = tuple(
            " & ".join(
                f"{k} == {repr(v)}" for k, v in zip(demographics_shape, shape_combo)
            )
            + " & "
            + color_query  # dependent on color!
            for shape_combo in shape_combos
            for color_query in color_queries
        )
    means: tuple[float, ...] = tuple(
        answers_df.query(query)[attachment_style].mean() for query in queries
    )

    # construct the plot
    vertex_names: tuple[str, ...] = tuple(
        " ".join(shape_combo)
        for shape_combo in shape_combos
        for color_combo in color_combos
    )
    color_names: tuple[str, ...] = tuple(
        " ".join(color_combo)
        for shape_combo in shape_combos
        for color_combo in color_combos
    )
    fig = px.line_polar(
        r=means,
        theta=vertex_names,
        color=color_names,
        line_close=True,
        # labels={"color": " ".join(demographics_color)},
        # template="plotly_dark",
        title="Spider Chart",
        width=400,
        height=250,
    )
    fig.update_layout(
        title_x=0.5,
        title_y=0.98,
        margin=dict(t=30),
        polar=dict(angularaxis=dict(showticklabels=False)),
        showlegend=False,
    )

    return fig


# spider graph
@callback(
    Output("spider-chart", "figure"),
    [
        Input("spider-attachment-style-dropdown", "value"),
        Input("spider-shape-dropdown", "value"),
        Input("spider-color-dropdown", "value"),
        Input("data-store", "data"),
    ],
)
def update_spider_chart(
    attachment_style: str,
    demographics_shape: list[str],
    demographics_color: list[str],
    data,
) -> go.Figure:
    answers_df = pd.DataFrame(data)
    # if no options are chosen return empty figure
    if not demographics_shape:
        return px.line_polar()

    # for the chosen demographics get the tuples with corresponding values
    shape_options: tuple[tuple[str, ...], ...] = tuple(
        demographics_values[demographic] for demographic in demographics_shape
    )
    color_options: tuple[tuple[str, ...], ...] = tuple(
        demographics_values[demographic] for demographic in demographics_color
    )

    # create cartesian products representing all possible combinations
    color_combos: tuple[tuple[str, ...], ...] = tuple(itertools.product(*color_options))
    shape_combos: tuple[tuple[str, ...], ...] = tuple(itertools.product(*shape_options))

    # construct the queries
    if not demographics_color:  # without color
        queries: tuple[str, ...] = tuple(
            " & ".join(
                f"{k} == {repr(v)}" for k, v in zip(demographics_shape, shape_combo)
            )
            for shape_combo in shape_combos
        )
    else:  # with color
        color_queries: tuple[str, ...] = tuple(
            " & ".join(
                f"{k} == {repr(v)}" for k, v in zip(demographics_color, color_combo)
            )
            for color_combo in color_combos
        )
        queries: tuple[str, ...] = tuple(
            " & ".join(
                f"{k} == {repr(v)}" for k, v in zip(demographics_shape, shape_combo)
            )
            + " & "
            + color_query  # dependent on color!
            for shape_combo in shape_combos
            for color_query in color_queries
        )
    means: tuple[float, ...] = tuple(
        answers_df.query(query)[attachment_style].mean() for query in queries
    )

    # construct the plot
    vertex_names: tuple[str, ...] = tuple(
        " ".join(shape_combo)
        for shape_combo in shape_combos
        for color_combo in color_combos
    )
    color_names: tuple[str, ...] = tuple(
        " ".join(color_combo)
        for shape_combo in shape_combos
        for color_combo in color_combos
    )
    fig = px.line_polar(
        r=means,
        theta=vertex_names,
        color=color_names,
        line_close=True,
        labels={"color": " ".join(demographics_color)},
        # template="plotly_dark",
    )

    return fig


# GLOBAL PIE CHART
# toggle pie modal
@callback(
    Output("pie-modal", "is_open"),
    [Input("pie-container", "n_clicks"), Input("close-pie", "n_clicks")],
    State("pie-modal", "is_open"),
)
def toggle_pie_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update pie thumbnail
@callback(
    Output("pie-thumbnail", "figure"),
    [
        Input("global-pie-chart-dropdown-attachment-style", "value"),
        Input("global-pie-chart-dropdown-demographic", "value"),
        Input("data-store", "data"),
    ],
)
def update_global_pie_thumbnail(
    attachment_style: str, demographic: str, data
) -> go.Figure:
    answers_df = pd.DataFrame(data)
    options: tuple[str, ...] = tuple(
        option for option in demographics_values[demographic]
    )
    values: tuple[float, ...] = tuple(
        answers_df[answers_df[demographic] == option][attachment_style].mean()
        for option in options
    )

    fig = px.pie(
        values=values,
        names=options,
        title="Global Pie Chart",
        width=400,
        height=250,
        # template="plotly_dark",
    )
    fig.update_layout(
        title_x=0.5,
        title_y=0.98,
        margin=dict(t=30),
        showlegend=False,
    )

    return fig


# update pie graph
@callback(
    Output("pie-graph", "figure"),
    [
        Input("global-pie-chart-dropdown-attachment-style", "value"),
        Input("global-pie-chart-dropdown-demographic", "value"),
        Input("data-store", "data"),
    ],
)
def update_global_pie_graph(attachment_style: str, demographic: str, data) -> go.Figure:
    answers_df = pd.DataFrame(data)
    options: tuple[str, ...] = tuple(
        option for option in demographics_values[demographic]
    )
    values: tuple[float, ...] = tuple(
        answers_df[answers_df[demographic] == option][attachment_style].mean()
        for option in options
    )

    fig = px.pie(
        values=values,
        names=options,
        title=f"{attachment_style.replace('_', ' ').capitalize()} distribution"
        f" by {demographic.replace('_', ' ')}",
        # template="plotly_dark",
    )

    return fig


# PARALLEL CATEGORIES
# toggle parallel modal
@callback(
    Output("parallel-modal", "is_open"),
    [Input("parallel-container", "n_clicks"), Input("close-parallel", "n_clicks")],
    State("parallel-modal", "is_open"),
)
def toggle_parallel_modal(open_modal, close_modal, is_open):
    if open_modal or close_modal:
        return not is_open
    return is_open


# update parallel thumbnail
@callback(
    Output("parallel-thumbnail", "figure"),
    [
        Input("parallel-categories-dropdown", "value"),
        Input("parallel-color-dropdown", "value"),
        Input("data-store", "data"),
    ],
)
def update_parallel_thumnail(selected_dims, color_by, data):
    answers_df = pd.DataFrame(data)
    if not selected_dims:
        selected_dims = ["gender"]
    fig = px.parallel_categories(
        answers_df,
        dimensions=selected_dims,
        color=color_by,
        color_continuous_scale=px.colors.sequential.Inferno,
        title="Parallel Categories Diagram",
        width=400,
        height=250,
    )
    fig.update_layout(
        title_x=0.5,
        title_y=0.98,
        margin=dict(t=30),
        showlegend=False,
    )
    fig.update_coloraxes(showscale=False)
    for dim in fig.data[0]["dimensions"]:
        dim["label"] = ""
    return fig


# update parallel graph
@callback(
    Output("parallel-graph", "figure"),
    [
        Input("parallel-categories-dropdown", "value"),
        Input("parallel-color-dropdown", "value"),
        Input("data-store", "data"),
    ],
)
def update_parallel_graph(selected_dims, color_by, data):
    answers_df = pd.DataFrame(data)
    if not selected_dims:
        selected_dims = ["gender"]
    if color_by == "any":
        fig = px.parallel_categories(
            answers_df,
            dimensions=selected_dims,
            color_continuous_scale=px.colors.sequential.Inferno,
            title="Parallel Categories Diagram",
        )
    else:
        fig = px.parallel_categories(
            answers_df,
            dimensions=selected_dims,
            color=color_by,
            color_continuous_scale=px.colors.sequential.Inferno,
            title="Parallel Categories Diagram",
        )
    return fig
