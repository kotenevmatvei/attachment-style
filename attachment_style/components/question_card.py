import dash_mantine_components as dmc
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
    visibleFrom="sm",
)

ProgressIndicatorMobile = dmc.Group(
    [
        dmc.Button(
            variant="light",
            color="gray",
            size="sm",
            pr=0,
            leftSection=DashIconify(icon="tabler:arrow-left", width=36),
            id="back-button-mobile",
            m=0,
            disabled=True,
        ),
        dmc.Badge(
            variant="light",
            color=constants.PRIMARY,
            size="lg",
            m=0,
            id="current-item-badge-mobile"
        ),
        dmc.Button(
            variant="light",
            color=constants.PRIMARY,
            size="sm",
            pl=0,
            m=0,
            rightSection=DashIconify(icon="tabler:arrow-right", width=36),
            id="forward-button-mobile",
            disabled=True,
        ),
    ],
    justify="space-between",
    hiddenFrom="sm",
)

QuestionCard = dmc.Card(
    id="question-card",
    shadow="sm",
    p="lg",
    radius="md",
    withBorder=True,
)

BottomActionButtons = dmc.Group(
    [
        dmc.Button(
            "Previous",
            variant="light",
            size="md",
            color="gray",
            leftSection=DashIconify(icon="tabler:chevron-left", width=16),
            id="prev-button",
            disabled=True,
        ),
        dmc.Button(
            "Next",
            # variant="default",
            size="md",
            w="15%",
            fw="bold",
            rightSection=DashIconify(icon="tabler:chevron-right", width=16),
            color=constants.PRIMARY,
            id="next-button",
            disabled=True,
        ),
    ],
    justify="space-between",
    mt="xl",
    visibleFrom="sm",
)

BottomActionButtonsMobile = dmc.Group(
    [
        dmc.Button(
            variant="light",
            size="sm",
            pr=0,
            m=0,
            color="gray",
            leftSection=DashIconify(icon="tabler:arrow-left", width=36),
            id="prev-button-mobile",
            disabled=True,
        ),
        dmc.Button(
            # variant="default",
            size="sm",
            pl=0,
            m=0,
            rightSection=DashIconify(icon="tabler:arrow-right", width=36),
            color=constants.PRIMARY,
            id="next-button-mobile",
            disabled=True,
        ),
    ],
    justify="space-between",
    mt="xl",
    hiddenFrom="sm",
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
    size={"base": "xl", "sm": "md"},
    px={"base": 0, "sm": "xl"},
    py="lg",
    children=[
        dmc.Title(
            "Questionnaire",
            order=1,
            ta="center",
            c=constants.PRIMARY,
            mb="xl",
        ),
        dmc.Stack(
            [
                ProgressIndicator,
                ProgressIndicatorMobile,
                ProgressBar,
                QuestionCard,
                dmc.Container(
                    w="90%",
                    children=ResponseOptions,
                ),
                # Action buttons
                BottomActionButtons,
                BottomActionButtonsMobile,
            ],
            gap="lg",
        )
    ],
)
