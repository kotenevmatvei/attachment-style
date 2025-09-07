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
            disabled=True,
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
            disabled=True,
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
        dmc.Button(
            option,
            id=f"option-{i}",
            w="100%",
            justify="left",
            fw="bold",
            size="md",
            className="option-flash",
            style={"boxShadow": "0 4px 4px rgba(0,0,0,0.10)"},
            radius="lg"
        )
        for i, option in enumerate(options, start=1)
    ],
    gap="md",
)

QuestionComponent = dmc.Container(
    [
        dmc.Container(
            [
                dmc.Title(
                    "Questionnaire",
                    order=1,
                    ta="center",
                    c=constants.PRIMARY,
                    mb="xl",
                ),
                dmc.Stack(
                    [
                        # Progress and navigation
                        ProgressIndicator,
                        # Progress bar
                        ProgressBar,
                        # Question card
                        QuestionCard,
                        # Response options
                        dmc.Container(
                            w="90%",
                            children=ResponseOptions,
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
                                    disabled=True,
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
                                    disabled=True,
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
                                disabled=True,
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


