import dash_mantine_components as dmc
from dash_iconify import DashIconify

import constants
from data.options import (
    therapy_labels_values,
    gender_labels_values,
    relationship_labels_values,
)

Demographics = dmc.Container(
    size="xl",
    py={"base": "xs", "sm": "xl"},
    children=[
        dmc.Title(
            "Demographics",
            order=1,
            ta="center",
            c=constants.PRIMARY,
            mb={"base": "xs", "sm": "xl"},
        ),
        dmc.Text(
            "Please fill in the following information for the person to be tested:",
            ta="center",
            c="dimmed",
            size="lg",
            mb={"base": "xs", "sm": "xl"},
        ),
        dmc.Paper(
            children=[
                dmc.SimpleGrid(
                    cols={"base": 1, "sm": 2},
                    spacing={"base": "xs", "sm": "lg"},
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Text("Age", fw=500, size="sm", c="gray.7"),
                                dmc.Select(
                                    id="age-select",
                                    placeholder="Select age",
                                    data=[str(i) for i in range(16, 121)],
                                    size="lg",
                                    radius="md",
                                    leftSection=DashIconify(icon="tabler:calendar", width=20),
                                ),
                            ],
                            gap="xs",
                        ),

                        # Relationship status
                        dmc.Stack(
                            children=[
                                dmc.Text("Relationship status", fw=500, size="sm", c="gray.7"),
                                dmc.Select(
                                    id="relationship-status-select",
                                    placeholder="Select relationship status",
                                    data=relationship_labels_values,
                                    size="lg",
                                    radius="md",
                                    leftSection=DashIconify(icon="tabler:heart", width=20),
                                ),
                            ],
                            gap="xs",
                        ),

                        # Therapy experience
                        dmc.Stack(
                            children=[
                                dmc.Text("Therapy experience", fw=500, size="sm", c="gray.7"),
                                dmc.Select(
                                    id="therapy-experience-select",
                                    placeholder="Select therapy experience",
                                    data=therapy_labels_values,
                                    size="lg",
                                    radius="md",
                                    leftSection=DashIconify(icon="tabler:brain", width=20),
                                ),
                            ],
                            gap="xs",
                        ),

                        # Gender
                        dmc.Stack(
                            children=[
                                dmc.Text("Gender", fw=500, size="sm", c="gray.7"),
                                dmc.Select(
                                    id="gender-select",
                                    placeholder="Select gender",
                                    data=gender_labels_values,
                                    size="lg",
                                    radius="md",
                                    leftSection=DashIconify(icon="tabler:user", width=20),
                                ),
                            ],
                            gap="xs",
                        ),
                    ],
                ),
            ],
            p="xl",
            radius="lg",
            shadow="sm",
            withBorder=True,
        ),

        # desktop
        dmc.Center(
            dmc.Button(
                "Continue to the test",
                id="continue-to-test-button",
                size="lg",
                radius="xl",
                leftSection=DashIconify(icon="tabler:arrow-right", width=20),
                variant="gradient",
                gradient={"from": constants.PRIMARY, "to": "cyan"},
                mt={"base": "xs", "sm": "xl"},
                px="xl",
            ),
            mt={"base": "lg", "sm": "xl"},
            # visibleFrom="sm",
        ),

        # # mobile
        # dmc.Center(
        #     dmc.Button(
        #         "To the test",
        #         id="continue-to-test-button-mobile",
        #         size="lg",
        #         radius="xl",
        #         leftSection=DashIconify(icon="tabler:arrow-right", width=20),
        #         variant="gradient",
        #         gradient={"from": constants.PRIMARY, "to": "cyan"},
        #         mt={"base": "xs", "sm": "xl"},
        #         # px="xl",
        #     ),
        #     mt="lg",
        #     hiddenFrom="sm",
        # ),
    ],
)
