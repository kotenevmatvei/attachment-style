import dash_mantine_components as dmc
from dash import Dash, _dash_renderer, callback, Input, Output, State, dcc, html
from dash_iconify import DashIconify
import constants

# Theme toggle button
theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    variant="transparent",
    color="yellow",
    id="color-scheme-toggle",
    size="lg",
)

header = dmc.Container(
    dmc.Group(
        [
            # Logo/Brand as clickable link (bigger title)
            html.Div(
                dmc.Anchor(
                    dmc.Group(
                        [
                            DashIconify(icon="tabler:brand-python", width=40, color=constants.PRIMARY),
                            dmc.Text("Attachment Style Test", size="2rem", fw=900, c=constants.PRIMARY),
                        ],
                        gap="sm",
                    ),
                    href="/",
                    underline=False,
                ),
                id="logo-div",
            ),
            # Right side: Navigation links and theme toggle
            dmc.Group(
                [
                    # Navigation links
                    dmc.Group(
                        [
                            html.Div(
                                dmc.Anchor(
                                    "Test", href="/", underline=False, c="dimmed", fw=500,
                                ),
                                id="test-anchor-header",
                            ),
                            # dmc.Anchor(
                            #     "Assess Yourself",
                            #     href="/test",
                            #     underline=False,
                            #     c="dimmed",
                            #     fw=500,
                            # ),
                            # dmc.Anchor(
                            #     "Assess Others",
                            #     href="/assess-others",
                            #     underline=False,
                            #     c="dimmed",
                            #     fw=500,
                            # ),
                            dmc.Anchor(
                                "Dashboard",
                                href="/simple-dashboard",
                                underline=False,
                                c="dimmed",
                                fw=500,
                            ),
                            dmc.Anchor(
                                "About",
                                href="/about",
                                underline=False,
                                c="dimmed",
                                fw=500,
                            ),
                        ],
                        gap="xl",
                        visibleFrom="sm",  # Hide on small screens
                    ),
                    # Mobile menu for small screens
                    dmc.Menu(
                        [
                            dmc.MenuTarget(
                                dmc.ActionIcon(
                                    DashIconify(icon="tabler:menu-2", width=20),
                                    variant="light",
                                    size="lg",
                                    hiddenFrom="sm",  # Only show on small screens
                                )
                            ),
                            dmc.MenuDropdown(
                                [
                                    dmc.MenuItem(
                                        "Home",
                                        leftSection=DashIconify(icon="tabler:home"),
                                    ),
                                    dmc.MenuItem(
                                        "Analytics",
                                        leftSection=DashIconify(
                                            icon="tabler:chart-bar"
                                        ),
                                    ),
                                    dmc.MenuItem(
                                        "Reports",
                                        leftSection=DashIconify(
                                            icon="tabler:file-text"
                                        ),
                                    ),
                                    dmc.MenuItem(
                                        "Settings",
                                        leftSection=DashIconify(icon="tabler:settings"),
                                    ),
                                ]
                            ),
                        ]
                    ),
                    # Theme toggle
                    theme_toggle,
                ],
                gap="md",
            ),
        ],
        justify="space-between",
        align="center",
        h="100%",
    ),
    size="1700px",  # Custom max width
    px="md",
    pt="lg",
    style={"width": "100%"},  # Ensures it takes full width until max-width is reached
)



