import dash_mantine_components as dmc
from dash import Dash, callback, Input, Output, State, dcc, page_container
from dash_iconify import DashIconify

from components.header_revised import header
from components.question_card import QuestionCard

# Set React version for DMC 0.14+
# _dash_renderer._set_react_version("18.2.0")

# Required stylesheets for full DMC functionality
stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

app = Dash(__name__, external_stylesheets=stylesheets, use_pages=True)

app_shell = dmc.AppShell(
    [
        dmc.AppShellHeader(header, h=80),
        dmc.AppShellMain(
            dmc.Container(
                [
                    # dmc.Title("Assess Yourself", order=1, mt="xl"),
                    page_container,

                    # dmc.Text(
                    #     "This is your main content area.",
                    #     size="lg",
                    #     c="dimmed",
                    #     mt="md",
                    # ),
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


if __name__ == "__main__":
    # app.run_server(host="0.0.0.0", port=8080)
    app.run(debug=True)
