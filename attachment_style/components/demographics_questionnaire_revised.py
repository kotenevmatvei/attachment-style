import dash_mantine_components as dmc
from dash_iconify import DashIconify
from data.options import (
    therapy_labels_values,
    gender_labels_values,
    relationship_labels_values,
)

DemographicsQuestionnaire = dmc.Container(
    size="xl",
    py="xl",
    children=[
        # Page title at the top
        dmc.Title(
            "Assess Yourself",
            order=1,
            ta="center",
            c="gray.8",
            mb="xl",
        ),
        
        # Enhanced header section with corrected text
        dmc.Stack(
            children=[
                dmc.Title(
                    "Help us understand your background",
                    order=2,
                    ta="center",
                    c="gray.7",
                    mb="xs",
                ),
                dmc.Text(
                    "This information helps us create your personalized dashboard",  # Updated text
                    ta="center",
                    c="dimmed",
                    size="lg",
                    mb="xl",
                ),
            ],
            gap="xs",
        ),
        
        # Enhanced form section with cards
        dmc.Paper(
            children=[
                dmc.SimpleGrid(
                    cols={"base": 1, "sm": 2},
                    spacing="lg",
                    children=[
                        # Age input
                        dmc.Stack(
                            children=[
                                dmc.Text("Age", fw=500, size="sm", c="gray.7"),
                                dmc.NumberInput(
                                    placeholder="How old are you?",
                                    min=10,
                                    max=120,
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
                                    placeholder="Select your status",
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
                                    placeholder="Select your experience level",
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
        
        # Enhanced button section
        dmc.Center(
            dmc.Button(
                "Continue to the test",
                size="lg",
                radius="xl",
                leftSection=DashIconify(icon="tabler:arrow-right", width=20),
                variant="gradient",
                gradient={"from": "blue", "to": "cyan"},
                mt="xl",
                px="xl",
            ),
            mt="xl",
        ),
    ],
)

