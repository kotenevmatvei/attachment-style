from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from data.options import demographics_labels_values, attachment_style_labels_values
import pandas as pd
import plotly.express as px

SpiderModal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Spider Chart")),
        dbc.ModalBody(
            [
                html.Label("Select the attachment style:"),
                dcc.Dropdown(
                    id="spider-attachment-style-dropdown",
                    options=attachment_style_labels_values,
                    clearable=False,
                    value="anxious_score",
                ),
                html.Label(
                    "Select Demographic Grouping for the shape " "(at least one):"
                ),
                dcc.Dropdown(
                    id="spider-shape-dropdown",
                    options=demographics_labels_values,
                    value=["gender", "relationship_status"],
                    clearable=False,
                    multi=True,
                ),
                html.Label("Select Demographic Grouping for the color:"),
                dcc.Dropdown(
                    id="spider-color-dropdown",
                    options=demographics_labels_values,
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
)

SpiderThumbnail = (
    html.Div(
        dcc.Graph(
            id="spider-thumbnail",
            config={"staticPlot": True},
            style={"cursor": "pointer"},
        ),
        id="spider-container",
        className="thumbnail",
    )
)


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
        Input("window-width", "data"),
    ],
)
def update_spider_thumbnail(
    attachment_style: str,
    demographics_shape: list[str],
    demographics_color: list[str],
    data,
    window_width,
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
    if window_width[0] > 500:
        fig = px.line_polar(
            r=means,
            theta=vertex_names,
            color=color_names,
            line_close=True,
            # labels={"color": " ".join(demographics_color)},
            # template="plotly_dark",
            title="Spider Chart",
            width=300,
            height=250,
        )
        fig.update_layout(
            title_x=0.5,
            title_y=0.98,
            margin=dict(t=30, r=0, l=0),
            polar=dict(angularaxis=dict(showticklabels=False)),
            showlegend=False,
        )
    else:
        fig = px.line_polar(
            r=means,
            theta=vertex_names,
            color=color_names,
            line_close=True,
            # labels={"color": " ".join(demographics_color)},
            # template="plotly_dark",
            title="Spider Chart",
            width=180,
            height=180,
        )
        fig.update_layout(
            title_font_size=15,
            title_x=0.5,
            title_y=0.95,
            margin=dict(t=30, r=0, l=0),
            polar=dict(
                angularaxis=dict(showticklabels=False),
                radialaxis=dict(showticklabels=False),
            ),
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
