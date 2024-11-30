import itertools 
import dash
import pandas as pd
import dash  # type: ignore

from dash import dcc, html, register_page, callback  # type: ignore
from dash.dependencies import Input, Output  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore

from attachment_style.utils.utils import get_data_from_db, aggregate_scores  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore

register_page(__name__)

df1: pd.DataFrame
df2: pd.DataFrame

df1, df2 = get_data_from_db(test=True)
df1, df2 = aggregate_scores(df1, df2)
answers_df = df1

# Get unique values for dropdown options
attachment_styles = ["avoidant_score", "secure_score", "anxious_score"]
therapy_experiences = answers_df["therapy_experience"].unique().tolist()
genders = answers_df["gender"].unique().tolist()
relationship_statuses = answers_df["relationship_status"].unique().tolist()

all_radar_options: dict[str, str] = {
    "Gender": "gender",
    "Therapy Experience": "therapy_experience",
    "Relationship Status": "relationship_status",
}

demographics_options: dict[str, tuple[str, ...]] = {
    "gender": ("male", "female", "other"),
    "therapy_experience": ("extensive", "some", "none"),
    "relationship_status": ("married", "in_relationship", "single"),
}


# App layout
def layout(**kwargs):
    return html.Div(
        [
            html.H3(
                "Attachment Style Quiz Results Dashboard", style={"textAlign": "center"}
            ),
            dcc.Checklist(
                ["Include test data"],
                ["Include test data"],
                id="include_test_data",
            ),
            dcc.Tabs(
                [
                    dcc.Tab(
                        label="Box Plot",
                        children=[
                            html.Div(
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
                                    ),
                                    html.Label("Select Attachment Style:"),
                                    dcc.Dropdown(
                                        id="attachment-style-dropdown-demographics",
                                        options=[
                                            {
                                                "label": style.split("_")[
                                                    0
                                                ].capitalize(),
                                                "value": style,
                                            }
                                            for style in attachment_styles
                                        ],
                                        value="avoidant_score",
                                    ),
                                    dcc.Graph(id="demographic-boxplot"),
                                ]
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Scatter Plot",
                        children=[
                            html.Div(
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
                        ],
                    ),
                    dcc.Tab(
                        label="Distributions",
                        children=[
                            html.Div(
                                [
                                    html.Label("Select Attachment Style:"),
                                    dcc.Dropdown(
                                        id="attachment-style-dropdown",
                                        options=[
                                            {
                                                "label": style.split("_")[
                                                    0
                                                ].capitalize(),
                                                "value": style,
                                            }
                                            for style in attachment_styles
                                        ],
                                        value="avoidant_score",
                                    ),
                                    dcc.Graph(id="distribution-histogram"),
                                ]
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Radar Chart",
                        children=[
                            html.Div(
                                [
                                    html.Label("Select the attachment style:"),
                                    dcc.Dropdown(
                                        id="radar-attachment-style-dropdown",
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
                                        id="radar-shape-dropdown",
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
                                    html.Label(
                                        "Select Demographic Grouping for the color:"
                                    ),
                                    dcc.Dropdown(
                                        id="radar-color-dropdown",
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
                                    dcc.Graph(id="radar-chart"),
                                ]
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="3D Chart",
                        children=[
                            html.Div(
                                [
                                    html.Label("Color by:"),
                                    dcc.Dropdown(
                                        id="3d-color-dropdown",
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
                                        value="therapy_experience",
                                    ),
                                    html.Label("Symbol by:"),
                                    dcc.Dropdown(
                                        id="3d-symbol-dropdown",
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
                                    ),
                                    dcc.Graph(id="cluster-plot"),
                                ]
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Parallel Categories",
                        children=[
                            html.Div(
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
                                                "label": style.split("_")[
                                                    0
                                                ].capitalize(),
                                                "value": style,
                                            }
                                            for style in attachment_styles
                                        ],
                                        value="secure_score",
                                    ),
                                    dcc.Graph(id="parallel-categories"),
                                ]
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Global Pie Chart",
                        children=[
                            html.Div(
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
                                    dcc.Graph(id="global-pie-chart-graph"),
                                ]
                            )
                        ],
                    ),
                ]
            ),
            dcc.Store(id="data_store", data={})
        ]
    )

# load the data from db
@callback(
    Output("data_store", "data"),
    [
        Input("include_test_data", "value"),

    ]
)
def include_test_data(include_test_data):
    if include_test_data == ["Include test data"]:
        df1, df2 = get_data_from_db(test=True)
        df1, df2 = aggregate_scores(df1, df2)
        answers_dict = df1.to_dict()
        print(answers_dict)
        return answers_dict
    df1, df2 = get_data_from_db(test=False)
    df1, df2 = aggregate_scores(df1, df2)
    answers_dict = df1.to_dict()
    print(answers_dict)
    return answers_dict
    

# Callbacks for interactivity
@callback(
    Output("distribution-histogram", "figure"),
    [
        Input("attachment-style-dropdown", "value"),
        Input("data_store", "data"),
    ]
)
def update_distribution(selected_style, data):
    answers_df = pd.DataFrame(data)
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
    Output("demographic-boxplot", "figure"),
    [
        Input("demographic-radio", "value"),
        Input("attachment-style-dropdown-demographics", "value"),
        Input("data_store", "data"),
    ],
)
def update_demographic_boxplot(demographic, selected_style, data):
    answers_df = pd.DataFrame(data)
    # print(answers_df)
    fig = px.box(
        answers_df,
        x=demographic,
        y=selected_style,
        title=f'{selected_style.split("_")[0].capitalize()} Attachment Scores by {demographic.replace("_", " ").title()}',
    )
    fig.update_xaxes(title=demographic.replace("_", " ").title())
    fig.update_yaxes(
        title=selected_style.split("_")[0].capitalize() + " Attachment Score"
    )
    return fig


@callback(
    Output("scatter-plot", "figure"),
    [
        Input("scatter-x-dropdown", "value"),
        Input("scatter-y-dropdown", "value"),
        Input("scatter-color-dropdown", "value"),
        Input("data_store", "data"),
    ],
)
def update_scatter_plot(x_var, y_var, color_var, data):
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


# only suggest by-color demographic options that have not already been chosen for shape.
@callback(
    Output("radar-color-dropdown", "options"),
    [
        Input("radar-shape-dropdown", "value"),
    ],
)
def update_radar_color_options(used_shape_options: list[str]) -> list[dict[str, str]]:
    not_used_options = [
        {"label": key, "value": val}
        for key, val in all_radar_options.items()
        if val not in used_shape_options
    ]
    return not_used_options


# render the radar chart based on the chosen options
@callback(
    Output("radar-chart", "figure"),
    [
        Input("radar-attachment-style-dropdown", "value"),
        Input("radar-shape-dropdown", "value"),
        Input("radar-color-dropdown", "value"),
        Input("data_store", "data"),
    ],
)
def update_radar_chart(
    attachment_style: str, 
    demographics_shape: list[str], 
    demographics_color: list[str],
    data,
) -> go.Figure:
    answers_df = pd.DataFrame(data)
    # if no options are chosen return empty figure
    if not demographics_shape:
        return px.line_polar(template="plotly_dark")

    # for the chosen demographics get the tuples with corresponding values
    shape_options: tuple[tuple[str, ...], ...] = tuple(
        demographics_options[demographic] for demographic in demographics_shape
    )
    color_options: tuple[tuple[str, ...], ...] = tuple(
        demographics_options[demographic] for demographic in demographics_color
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
        template="plotly_dark",
    )

    return fig


@callback(
    Output("cluster-plot", "figure"),
    [
        Input("3d-color-dropdown", "value"), 
        Input("3d-symbol-dropdown", "value"),
        Input("data_store", "data"),
    ],
)
def update_3d_plot(color, symbol, data):
    answers_df = pd.DataFrame(data)
    # X = df[["avoidant_score", "secure_score", "anxious_score"]]
    # kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
    # df["cluster"] = kmeans.labels_
    fig = px.scatter_3d(
        answers_df,
        x="avoidant_score",
        y="secure_score",
        z="anxious_score",
        color=color,
        symbol=symbol,
        title=f"3D-Chart",
    )
    fig.update_layout(
        scene=dict(
            xaxis_title="Avoidant",
            yaxis_title="Secure",
            zaxis_title="Anxious",
        )
    )
    return fig


@callback(
    Output("parallel-categories", "figure"),
    [
        Input("parallel-categories-dropdown", "value"),
        Input("parallel-color-dropdown", "value"),
        Input("data_store", "data"),
    ],
)
def update_parallel_categories(selected_dims, color_by, data):
    answers_df = pd.DataFrame(data)
    if not selected_dims:
        selected_dims = ["gender"]
    fig = px.parallel_categories(
        answers_df,
        dimensions=selected_dims,
        color=color_by,
        color_continuous_scale=px.colors.sequential.Inferno,
        title="Parallel Categories Diagram",
    )
    return fig


@callback(
    Output("global-pie-chart-graph", "figure"),
    [
        Input("global-pie-chart-dropdown-attachment-style", "value"),
        Input("global-pie-chart-dropdown-demographic", "value"),
        Input("data_store", "data"),
    ],
)
def update_global_pie_chart(attachment_style: str, demographic: str, data) -> go.Figure:
    answers_df = pd.DataFrame(data)
    options: tuple[str, ...] = tuple(
        option for option in demographics_options[demographic]
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
        template="plotly_dark",
    )

    return fig

