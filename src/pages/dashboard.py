import itertools

import dash
from dash import dcc, html, register_page, callback
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
from sklearn.cluster import KMeans
from utils.utils import get_data_from_db, aggregate_scores
import dash_bootstrap_components as dbc

register_page(__name__)

df1, df2 = get_data_from_db()
df1, df2 = aggregate_scores(df1, df2)
df = df1

# Initialize the app
app = dash.Dash(__name__)



# Get unique values for dropdown options
attachment_styles = ["avoidant_score", "secure_score", "anxious_score"]
therapy_experiences = df["therapy_experience"].unique().tolist()
genders = df["gender"].unique().tolist()
relationship_statuses = df["relationship_status"].unique().tolist()


# App layout
def layout(**kwargs):
    return html.Div(
    [
        html.H3(
            "Attachment Style Quiz Results Dashboard", style={"textAlign": "center"}
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
                                            "label": style.split("_")[0].capitalize(),
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
                                            "label": style.split("_")[0].capitalize(),
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
                                    id="radar-style-dropdown",
                                    options=[
                                        {"label": "Anxious", "value": "anxious_score"},
                                        {"label": "Secure", "value": "secure_score"},
                                        {"label": "Avoidant", "value": "avoidant_score"},
                                    ],
                                    value="anxious_score",
                                ),
                                html.Label("Select Demographic Grouping for the shape:"),
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
                                    multi=True,
                                ),
                                html.Label("Select Demographic Grouping for the color:"),
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
                                    value="therapy_experience",
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
                                            "label": style.split("_")[0].capitalize(),
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
            ]
        ),
    ]
)


# Callbacks for interactivity
@callback(
    Output("distribution-histogram", "figure"),
    Input("attachment-style-dropdown", "value"),
)
def update_distribution(selected_style):
    fig = px.histogram(
        df,
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
    ],
)
def update_demographic_boxplot(demographic, selected_style):
    fig = px.box(
        df,
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
    ],
)
def update_scatter_plot(x_var, y_var, color_var):
    if color_var == "None":
        fig = px.scatter(
            df,
            x=x_var,
            y=y_var,
            title=f'{y_var.split("_")[0].capitalize()} vs {x_var.capitalize()}',
        )
    else:
        fig = px.scatter(
            df,
            x=x_var,
            y=y_var,
            color=color_var,
            title=f'{y_var.split("_")[0].capitalize()} vs {x_var.capitalize()} Colored by {color_var.replace("_", " ").title()}',
        )
    fig.update_xaxes(title=x_var.replace("_", " ").title())
    fig.update_yaxes(title=y_var.replace("_", " ").title())
    return fig


@callback(
    Output("radar-chart", "figure"),
    [Input("radar-style-dropdown", "value"),
     Input("radar-shape-dropdown", "value"),
     Input("radar-color-dropdown", "value")]
)
def update_radar_chart(style, demographics_shape, demographics_color):
    values = (df[demographic].unique() for demographic in demographics_shape)
    categories = list(itertools.product(*values))
    colors = df[demographics_color].unique()
    print(colors)
    fig = go.Figure()
    for color in colors:
        if len(demographics_shape) == 1:
            r = [
                df[(df[demographics_shape[0]] == combo[0]) & (df[demographics_color] == color)][style].mean()
                for combo in categories
            ]
        elif len(demographics_shape) == 2:
            r = [
                df[(df[demographics_shape[0]] == combo[0]) & (df[demographics_shape[1]] == combo[1]) & (df[demographics_color] == color)][style].mean()
                for combo in categories
            ]
        else:
            raise ValueError("The input for radar chart shape accepts the maximum of 2 options")

        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=categories,
            fill="tonext",
            name=f"{demographics_color}: {color}"

        ))
    # fig.update_layout(
    #     polar=dict(
    #         radialaxis=dict(
    #             visible=True,
    #             range=[0, 10]
    #         )),
    #     showlegend=True
    # )
    # fig.update_layout(
    #     polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
    #     title=f'Average Attachment Scores by {demographic.replace("_", " ").title()}',
    # )
    return fig



@callback(Output("cluster-plot", "figure"),
          [Input("3d-color-dropdown", "value"),
           Input("3d-symbol-dropdown", "value")]
)
def update_3d_plot(color, symbol):
    # X = df[["avoidant_score", "secure_score", "anxious_score"]]
    # kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
    # df["cluster"] = kmeans.labels_
    fig = px.scatter_3d(
        df,
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
    ],
)
def update_parallel_categories(selected_dims, color_by):
    if not selected_dims:
        selected_dims = ["gender"]
    fig = px.parallel_categories(
        df,
        dimensions=selected_dims,
        color=color_by,
        color_continuous_scale=px.colors.sequential.Inferno,
        title="Parallel Categories Diagram",
    )
    return fig


# if __name__ == "__main__":
#     app.run_server(debug=True)
