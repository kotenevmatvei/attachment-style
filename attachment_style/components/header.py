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
            html.Div(
                dmc.Anchor(
                    dmc.Group(
                        [
                            DashIconify(icon="tabler:brand-python", width=40, color=constants.PRIMARY),
                            dmc.Text(
                                "Attachment Style Test",
                                fz={"base": "1.3rem", "xs": "1.5rem", "sm": "1.7rem", "md": "2rem"},
                                fw=900,
                                c=constants.PRIMARY,
                            ),
                        ],
                        gap="sm",
                    ),
                    href="/",
                    underline=False,
                ),
                id="logo-div",
            ),
            dmc.Group(
                [
                    dmc.Group(
                        [
                            html.Div(
                                dmc.Anchor(
                                    "Test", href="/", underline=False, c="dimmed", fw=500,
                                ),
                                id="test-anchor-header",
                            ),
                            dmc.Anchor(
                                "Dashboard",
                                href="/dashboard",
                                underline=False,
                                c="dimmed",
                                fw=500,
                            ),
                            dmc.Anchor(
                                "Feedback",
                                href="/feedback",
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
                                        "Test",
                                        leftSection=DashIconify(icon="tabler:home"),
                                        href="/"
                                    ),
                                    dmc.MenuItem(
                                        "Dashboard",
                                        leftSection=DashIconify(
                                            icon="tabler:chart-bar"
                                        ),
                                        href="/dashboard"
                                    ),
                                    dmc.MenuItem(
                                        "Feedback",
                                        leftSection=DashIconify(
                                            icon="tabler:file-text"
                                        ),
                                        href="/feedback"
                                    ),
                                    dmc.MenuItem(
                                        "About",
                                        leftSection=DashIconify(icon="tabler:clipboard-text"),
                                        href="/about"
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



