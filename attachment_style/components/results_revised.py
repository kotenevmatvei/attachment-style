import dash
import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import dcc, Input, Output, callback
from dash_iconify import DashIconify

import constants

app = dash.Dash(__name__)
dmc.add_figure_templates()

results_data = {
    "anxious_score": 65,
    "avoidant_score": 45,
    "secure_score": 80,
    "dominant_style": "Secure",
}


Chart = go.Figure(
        data=[
            go.Bar(
                x=["Anxious", "Avoidant", "Secure"],
                y=[
                    results_data["anxious_score"],
                    results_data["avoidant_score"],
                    results_data["secure_score"],
                ],
                marker_color=["#FA5252", "#20C997", "#339AF0"],
                text=[
                    f"{score}%"
                    for score in [
                        results_data["anxious_score"],
                        results_data["avoidant_score"],
                        results_data["secure_score"],
                    ]
                ],
                textposition="auto",
            )
        ]
    )


ScoreCards = dmc.SimpleGrid(
        cols=3,
        children=[
            # Anxious Score Card
            dmc.Paper(
                [
                    dmc.Stack(
                        [
                            dmc.Group(
                                [
                                    DashIconify(
                                        icon="tabler:heart-broken",
                                        width=24,
                                        color="#FA5252",
                                    ),
                                    dmc.Text("Anxious", fw=600, size="lg"),
                                ],
                                gap="xs",
                            ),
                            dmc.Text(
                                # f"{results_data['anxious_score']}%",
                                size="xl",
                                fw=700,
                                c="#FA5252",
                                id="anxious-score-percent-text",
                            ),
                            dmc.Text(
                                "Seeks closeness but worries about relationships",
                                size="sm",
                                c="dimmed",
                            ),
                        ],
                        gap="xs",
                    )
                ],
                p="md",
                radius="md",
                withBorder=True,
                shadow="sm",
            ),
            # Avoidant Score Card
            dmc.Paper(
                [
                    dmc.Stack(
                        [
                            dmc.Group(
                                [
                                    DashIconify(
                                        icon="tabler:shield", width=24, color="#20C997"
                                    ),
                                    dmc.Text("Avoidant", fw=600, size="lg"),
                                ],
                                gap="xs",
                            ),
                            dmc.Text(
                                # f"{results_data['avoidant_score']}%",
                                size="xl",
                                fw=700,
                                c="#20C997",
                                id="avoidant-score-percent-text",
                            ),
                            dmc.Text(
                                "Values independence and self-reliance",
                                size="sm",
                                c="dimmed",
                            ),
                        ],
                        gap="xs",
                    )
                ],
                p="md",
                radius="md",
                withBorder=True,
                shadow="sm",
            ),
            # Secure Score Card
            dmc.Paper(
                [
                    dmc.Stack(
                        [
                            dmc.Group(
                                [
                                    DashIconify(
                                        icon="tabler:heart", width=24, color="#339AF0"
                                    ),
                                    dmc.Text("Secure", fw=600, size="lg"),
                                ],
                                gap="xs",
                            ),
                            dmc.Text(
                                # f"{results_data['secure_score']}%",
                                size="xl",
                                fw=700,
                                c="#339AF0",
                                id="secure-score-percent-text",
                            ),
                            dmc.Text(
                                "Comfortable with intimacy and autonomy",
                                size="sm",
                                c="dimmed",
                            ),
                        ],
                        gap="xs",
                    )
                ],
                p="md",
                radius="md",
                withBorder=True,
                shadow="sm",
            ),
        ],
        spacing="md",
    )


ResultsInterpretation = dmc.Paper(
        [
            dmc.Stack(
                [
                    dmc.Group(
                        [
                            DashIconify(icon="tabler:bulb", width=28, color="#339AF0"),
                            dmc.Text("Your Results Interpretation", size="xl", fw=600),
                        ],
                        gap="sm",
                    ),
                    dmc.Alert(
                        children=[
                            dmc.Text(
                                [
                                    "Your dominant attachment style is ",
                                    dmc.Text(
                                        results_data["dominant_style"],
                                        fw=700,
                                        span=True,
                                        c="#339AF0",
                                    ),
                                    f" with a score of {results_data['secure_score']}%.",
                                ]
                            ),
                        ],
                        title="Primary Attachment Style",
                        icon=DashIconify(icon="tabler:info-circle"),
                        color=constants.PRIMARY,
                        variant="light",
                    ),
                    dmc.Text(
                        [
                            "People with a ",
                            dmc.Text("secure attachment style", fw=600, span=True),
                            " typically feel comfortable with intimacy and are usually warm and loving. They have "
                            "a positive view of themselves and their partners. They communicate effectively, are "
                            "comfortable depending on others and having others depend on them, and don't worry about "
                            "being alone or being accepted.",
                        ],
                        size="md",
                    ),
                    dmc.Divider(),
                    dmc.Text("Key Characteristics:", fw=600, size="md"),
                    dmc.List(
                        [
                            dmc.ListItem("Comfortable with emotional intimacy"),
                            dmc.ListItem("Effective communication skills"),
                            dmc.ListItem(
                                "Balanced need for independence and closeness"
                            ),
                            dmc.ListItem("Positive self-image and view of others"),
                            dmc.ListItem(
                                "Resilient in handling relationship conflicts"
                            ),
                        ],
                        icon=DashIconify(
                            icon="tabler:check", width=16, color="#51CF66"
                        ),
                    ),
                ],
                gap="md",
            )
        ],
        p="lg",
        radius="md",
        withBorder=True,
        shadow="sm",
    )


ResultsBoard = dmc.Container(
        [
            dmc.Stack(
                [
                    dmc.Center(
                        dmc.Title(
                            "Your Results", c=constants.PRIMARY,
                        ),
                    ),
                    ScoreCards,
                    # Chart
                    dmc.Paper(
                        [
                            dcc.Graph(
                                id="results-chart",
                                config={"displayModeBar": False},
                            )
                        ],
                        p="md",
                        radius="md",
                        withBorder=True,
                        shadow="sm",
                    ),
                    ResultsInterpretation,
                    dmc.Paper(
                        [
                            dmc.Stack(
                                [
                                    dmc.Group(
                                        [
                                            DashIconify(
                                                icon="tabler:download",
                                                width=28,
                                                color="#FD7E14",
                                            ),
                                            dmc.Text(
                                                "Download Your Results",
                                                size="lg",
                                                fw=600,
                                            ),
                                        ],
                                        gap="sm",
                                    ),
                                    dmc.Text(
                                        "Get a comprehensive PDF report with your attachment style analysis, "
                                        "detailed explanations, and personalized recommendations.",
                                        size="md",
                                        c="dimmed",
                                    ),
                                    dmc.Button(
                                        "Download PDF Report",
                                        size="lg",
                                        leftSection=DashIconify(
                                            icon="tabler:file-type-pdf", width=20
                                        ),
                                        color="orange",
                                        variant="gradient",
                                        gradient={"from": "orange", "to": "red"},
                                        id="download-pdf",
                                        fullWidth=True,
                                    ),
                                ],
                                gap="md",
                            )
                        ],
                        id="download-paper",
                        p="xl",
                        radius="md",
                        withBorder=True,
                        shadow="lg",
                    ),
                    dmc.Group(
                        [
                            dmc.Button(
                                "Retake Assessment",
                                variant="outline",
                                leftSection=DashIconify(
                                    icon="tabler:refresh", width=16
                                ),
                                id="retake-survey",
                            ),
                            dmc.Button(
                                "Share Results",
                                variant="light",
                                leftSection=DashIconify(icon="tabler:share", width=16),
                                id="share-results",
                            ),
                            dmc.Button(
                                "Learn More",
                                variant="light",
                                color="grape",
                                leftSection=DashIconify(icon="tabler:book", width=16),
                                id="learn-more",
                            ),
                        ],
                        justify="center",
                        gap="md",
                    ),
                ],
                gap="xl",
            )
        ],
        size="lg",
        px="xl",
        py="lg",
    )


# @callback(
#     Output("results-chart", "figure"),
#     Input("mantine-provider", "forceColorScheme"),
# )
# def update_chart_theme(color_scheme):
#     return create_results_chart(color_scheme)




@callback(
    Output("download-paper", "style"),
    Input("mantine-provider", "forceColorScheme"),
)
def update_download_paper_style(color_scheme):
    if color_scheme == "dark":
        return {
            "background": f"linear-gradient(135deg, {dmc.DEFAULT_THEME['colors']['dark'][8]} 0%, "
                          f"{dmc.DEFAULT_THEME['colors']['dark'][6]} 100%)"
        }
    return {"background": "linear-gradient(135deg, #FFF5F5 0%, #FFF8DC 100%)"}


@callback(
    Output("download-pdf", "loading"),
    Input("download-pdf", "n_clicks"),
    prevent_initial_call=True,
)
def handle_pdf_download(n_clicks):
    if n_clicks:
        return True
    return False


if __name__ == "__main__":
    app.run(debug=True)
