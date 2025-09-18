import dash_mantine_components as dmc
import constants

DashboardKPIs = dmc.Paper(
    [
        # Statistics in a grid instead of badges
        dmc.SimpleGrid(
            cols={"base": 2, "md": 4},
            children=[
                dmc.Paper(
                    [
                        dmc.Stack(
                            [
                                dmc.Text(
                                    "Anxious: 57%",
                                    size="xl",
                                    fw=700,
                                    ta="center",
                                    c=constants.PRIMARY,
                                    id="dominant-style-kpi",
                                ),
                                dmc.Text(
                                    "Dominant attachment style",
                                    size="sm",
                                    c="dimmed",
                                    ta="center",
                                ),
                            ],
                            gap=0,
                        ),
                    ],
                    p="md",
                    radius="md",
                    withBorder=True,
                ),
                dmc.Paper(
                    [
                        dmc.Stack(
                            [
                                dmc.Text(
                                    "Female: 48%",
                                    size="xl",
                                    fw=700,
                                    ta="center",
                                    c=constants.PRIMARY,
                                    id="dominant-gender-kpi",
                                ),
                                dmc.Text(
                                    "Dominant gender",
                                    size="sm",
                                    c="dimmed",
                                    ta="center",
                                ),
                            ],
                            gap=0,
                        ),
                    ],
                    p="md",
                    radius="md",
                    withBorder=True,
                ),
                dmc.Paper(
                    [
                        dmc.Stack(
                            [
                                dmc.Text(
                                    "Some: 49%",
                                    size="xl",
                                    fw=700,
                                    ta="center",
                                    c=constants.PRIMARY,
                                    id="dominant-therapy-experience-kpi",
                                ),
                                dmc.Text(
                                    "Dominant therapy experience",
                                    size="sm",
                                    c="dimmed",
                                    ta="center",
                                ),
                            ],
                            gap=0,
                        ),
                    ],
                    p="md",
                    radius="md",
                    withBorder=True,
                ),
                dmc.Paper(
                    [
                        dmc.Stack(
                            [
                                dmc.Text(
                                    "124",
                                    size="xl",
                                    fw=700,
                                    ta="center",
                                    c=constants.PRIMARY,
                                    id="total-submissions-kpi"
                                ),
                                dmc.Text(
                                    "Total Submissions",
                                    size="sm",
                                    c="dimmed",
                                    ta="center",
                                ),
                            ],
                            gap=0,
                        ),
                    ],
                    p="md",
                    radius="md",
                    withBorder=True,
                ),
            ],
            spacing="md",
        ),
    ],
    p="lg",
    radius="md",
    shadow="sm",
    withBorder=True,
    mb="xl",
)
