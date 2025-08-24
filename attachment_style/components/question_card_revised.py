import dash_mantine_components as dmc
from dash import dcc, Input, Output, callback
from dash_iconify import DashIconify

import constants

options = [
    "I strongly disagree",
    "Disagree",
    "Slightly disagree",
    "Neutral",
    "Slightly agree",
    "Agree",
    "I strongly agree",
]

ProgressBar = dmc.Paper(
    id="progress-bar",
    p=5,
    radius=50,
    shadow="lg",
    children=[
        dmc.Grid(
            columns=36,
            children=[
                dmc.GridCol(
                    dmc.Paper(" ", h=18, id={"type": "question-indicator", "index": i},radius="xl", shadow="xl"),
                    span=1
                )
                for i in range(1, 37)
            ],
            gutter=5,
            w="100%",
        )
    ]
)

ProgressIndicator = dmc.Group(
    [
        dmc.Button(
            "GO BACK",
            variant="light",
            color="gray",
            size="sm",
            leftSection=DashIconify(icon="tabler:arrow-left", width=16),
            id="back-button",
        ),
        dmc.Badge(
            variant="light",
            color=constants.PRIMARY,
            size="lg",
            id="current-item-badge"
        ),
        dmc.Button(
            "FORWARD",
            variant="light",
            color=constants.PRIMARY,
            size="sm",
            rightSection=DashIconify(icon="tabler:arrow-right", width=16),
            id="forward-button",
        ),
    ],
    justify="space-between",
)

QuestionCard = dmc.Paper(
    # this is necessary for the proper text alignment depending on the question set
    children=dmc.Flex(
        dcc.Markdown(id="question-markdown"),
        id="question-content-flex",
        h="100%",
        direction="column",
    ),
    id="question-paper",
    shadow="sm",
    p="lg",
    ta="center",
    radius="md",
    withBorder=True,
)

ResponseOptions = dmc.Stack(
    [
        dmc.Radio(
            id=f"option-{i}",
            label=option,
            value=str(i),
            size="md",
            styles={
                "root": {"padding": "12px 16px"},
                "body": {"alignItems": "center"},
                "label": {"fontSize": "16px", "fontWeight": 400},
            },
        )
        for i, option in enumerate(options)
    ],
    gap="xs",
)

QuestionComponent = dmc.Container(
    [
        dmc.Container(
            [
                dmc.Stack(
                    [
                        # Progress and navigation
                        ProgressIndicator,
                        # Progress bar
                        ProgressBar,
                        # Question card
                        QuestionCard,
                        # Response options
                        dmc.Paper(
                            [
                                dmc.RadioGroup(
                                    children=ResponseOptions,
                                    id="response-group",
                                    value=None,
                                    size="md",
                                )
                            ],
                            shadow="sm",
                            p="lg",
                            radius="md",
                            withBorder=True,
                            mt="lg",
                        ),
                        # Action buttons
                        dmc.Group(
                            [
                                dmc.Button(
                                    "Previous",
                                    variant="light",
                                    size="md",
                                    color="gray",
                                    leftSection=DashIconify(
                                        icon="tabler:chevron-left", width=16
                                    ),
                                    id="prev-button",
                                ),
                                dmc.Button(
                                    "Next",
                                    # variant="default",
                                    size="md",
                                    w="15%",
                                    fw="bold",
                                    rightSection=DashIconify(
                                        icon="tabler:chevron-right", width=16
                                    ),
                                    color=constants.PRIMARY,
                                    id="next-button",
                                    # disabled=True,  # Initially disabled until selection is made
                                ),
                            ],
                            justify="space-between",
                            mt="xl",
                        ),
                        dmc.Center(
                            dmc.Button(
                                "To Results",
                                id="to-results-button",
                                size="lg",
                                w="25%",
                                radius="xl",
                                leftSection=DashIconify(icon="tabler:arrow-right", width=20),
                                variant="gradient",
                                gradient={"from": constants.PRIMARY, "to": "cyan"},
                                mt="lg",
                                px="xl",
                            ),
                        ),
                    ],
                    gap="lg",
                )
            ],
            size="md",
            px="xl",
            py="lg",
        )
    ]
)


@callback(
    [
        Output("results-board-collapse", "opened"),
        Output("question-card-collapse", "opened", allow_duplicate=True),
    ],
    [
        Input("to-results-button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def toggle_results_collapse(to_results_click):
    if to_results_click:
        return True, False
    return False, True
