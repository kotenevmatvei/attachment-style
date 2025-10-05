import dash
import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify

import constants

app = dash.Dash(__name__)
dmc.add_figure_templates()

ScoreCards = dmc.Flex(
    # cols=3,
    children=[
        # Anxious Score Card
        dmc.Paper(
            [
                dmc.Stack(
                    [
                        dmc.Flex(
                            direction={"base": "row", "sm": "column"},
                            gap="sm",
                            children=[
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
                            ]
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
                        dmc.Flex(
                            direction={"base": "row", "sm": "column"},
                            gap="sm",
                            children=[
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
                            ]
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
                        dmc.Flex(
                            direction={"base": "row", "sm": "column"},
                            gap="sm",
                            children=[
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
                            ]
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
    # spacing="md",
    gap="md",
    direction={"base": "column", "sm": "row"},
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
                    id="dominant-style-text",
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
                    id="result-interpretation-text",
                ),
                dmc.Divider(),
                dmc.Text("Key Characteristics:", fw=600, size="md"),
                dmc.List(
                    id="result-interpretation-list",
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
        html.Div(id="dummy-div-pic-download"),
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
                                    id="download-report-button",
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
                        html.A(
                            dmc.Button(
                                "Retake Assessment",
                                variant="outline",
                                leftSection=DashIconify(
                                    icon="tabler:refresh", width=16
                                ),
                                id="retake-survey-button",
                            ),
                            href="/",
                        ),
                        html.A(
                            dmc.Button(
                                "Learn More",
                                variant="light",
                                color="grape",
                                leftSection=DashIconify(icon="tabler:book", width=16),
                                id="learn-more-button",
                            ),
                            href="/about",
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
