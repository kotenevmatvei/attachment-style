import dash_mantine_components as dmc
from dash import register_page, html

import constants

register_page(__name__, "/feedback")


def layout(**kwargs):
    return dmc.Container(
        children=[
            html.Div(id="dummy-email-div"),
            dmc.Center(
                dmc.Title("Please leave your feedback", c=constants.PRIMARY),
                mb="lg",
            ),
            dmc.Paper(
                withBorder=True,
                shadow="lg",
                p="lg",
                radius="lg",
                children=[
                    dmc.Title("Things you might consider:", order=4, ml="lg", mb={"base": "sm", "sm": 0}),
                    dmc.SimpleGrid(
                        cols={"base": 1, "sm": 2},
                        spacing=0,
                        children=[
                            dmc.List(
                                p={"base": 0, "sm": "lg"},
                                children=[
                                    dmc.ListItem(
                                        dmc.Text("Do the questions and the scoring make sense?")
                                    ),
                                    dmc.ListItem(
                                        dmc.Text("Is the dashboard intuitive?")
                                    ),
                                ]
                            ),
                            dmc.List(
                                p={"base": 0, "sm": "lg"},
                                children=[
                                    dmc.ListItem(
                                        dmc.Text("Did you experience any bugs in the website?")
                                    ),
                                    dmc.ListItem(
                                        dmc.Text("Do you have any other suggestions?")
                                    ),
                                ]
                            )
                        ]
                    ),
                    dmc.Textarea(
                        # label="Please leave your feedback here:",
                        mt={"base": "sm", "sm": 0},
                        c="dimmed",
                        placeholder="Leave your feedback here",
                        id="feedback-input",
                        minRows=8,
                        labelProps={
                            "style": {
                                "fontSize": "16px",
                            }
                        },
                        autosize=True,
                        size="xl",
                        mb="xl",
                    ),
                    dmc.Stack(
                        gap="xs",
                        children=[
                            dmc.Text(
                                "You may leave your email address here if you'd like me to get back to you",
                            ),
                            dmc.TextInput(
                                placeholder="Optional: email",
                                id="email-input",
                                w={"base": "100%", "sm": "60%"},
                            )
                        ]

                    ),
                ],
            ),
            dmc.Center(
                dmc.Button(
                    "Submit",
                    id="send-feedback-button",
                    size="lg",
                    radius="lg",
                ),
                pt="lg",
            )

        ]
    )
