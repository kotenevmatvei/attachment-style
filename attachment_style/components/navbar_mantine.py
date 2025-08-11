import dash_mantine_components as dmc
from dash import Dash, _dash_renderer, callback, Input, Output, State, dcc
from dash_iconify import DashIconify

# Set React version for DMC 0.14+
_dash_renderer._set_react_version("18.2.0")

# Required stylesheets for full DMC functionality
stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

app = Dash(external_stylesheets=stylesheets)

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

# Simplified navigation header
# Simplified navigation header with container
header = dmc.Container(
    dmc.Group(
        [
            # Logo/Brand as clickable link (bigger title)
            dmc.Anchor(
                dmc.Group(
                    [
                        DashIconify(icon="tabler:brand-python", width=40, color="blue"),
                        dmc.Text("My Dashboard", size="2rem", fw=900, c="blue"),
                    ],
                    gap="sm",
                ),
                href="/",
                underline=False,
            ),
            # Right side: Navigation links and theme toggle
            dmc.Group(
                [
                    # Navigation links
                    dmc.Group(
                        [
                            dmc.Anchor(
                                "Home", href="/", underline=False, c="dimmed", fw=500
                            ),
                            dmc.Anchor(
                                "Analytics",
                                href="/analytics",
                                underline=False,
                                c="dimmed",
                                fw=500,
                            ),
                            dmc.Anchor(
                                "Reports",
                                href="/reports",
                                underline=False,
                                c="dimmed",
                                fw=500,
                            ),
                            dmc.Anchor(
                                "Settings",
                                href="/settings",
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

# Simplified app shell (no sidebar)
app_shell = dmc.AppShell(
    [
        dmc.AppShellHeader(header, h=80),  # Slightly taller for bigger title
        dmc.AppShellMain(
            dmc.Container(
                [
                    dmc.Title("Welcome to Your Dashboard", order=1, mt="xl"),
                    dmc.Text(
                        "This is your main content area.",
                        size="lg",
                        c="dimmed",
                        mt="md",
                    ),
                ],
                size="xl",
                py="xl",
            )
        ),
    ],
    header={"height": 80},
    padding="md",
    id="app-shell",
)

# Main layout
app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="theme-store", storage_type="local", data="light"),
        app_shell,
    ],
    id="mantine-provider",
    forceColorScheme="light",
)


# Theme toggle callback
@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(_, theme):
    return "dark" if theme == "light" else "light"


if __name__ == "__main__":
    # app.run_server(host="0.0.0.0", port=8080)
    app.run(debug=True)
