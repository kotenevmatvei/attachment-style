import logging

import dash_mantine_components as dmc
from dash import Dash, dcc, page_container

import constants
from components.header_revised import header

from components.debug_footer import DebugFooter

from utils.utils import read_questions

from callbacks.test_page import subject, demographics, question_card

logging.basicConfig(
    level=logging.INFO,
    # format="{asctime} - {levelname} - {filename} - {funcName} - {message}",
    format="APP: {levelname} - {filename} - {funcName} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

# required stylesheets for full DMC functionality
stylesheets = [
    "https://unpkg.com/@mantine/core@7/styles.css",
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
        dcc.Store(id="subject-store"),
        # questions are stored as [("question-text", "corresponding-attachment-style"), (...), ...]
        dcc.Store(id="questions-store", data=read_questions("you")),
        dcc.Store(id="questions-len", data=36),
        dcc.Store(id="demographics-answers-store"),
        # answers are stored as
        # {"question-ind": ("attachment-style", value, "question-text"), "question-ind+1": (...), ...}
        dcc.Store(id="answers-store", data={}),
        dcc.Store(id="questions-answered-count-store", data=1),
        dcc.Store(id="current-question-count-store", data=1),
        dcc.Store(id="last-question-visited", data=False),
        dmc.AppShellHeader(header, h=80),
        dmc.AppShellMain(
            dmc.Container(
                [
                    page_container,
                    DebugFooter,
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
    id="mantine-provider",
    forceColorScheme="light",
    theme={"colors": {"steel_blue": constants.STEEL_BLUE_SHADES},
           "primaryColor": "steel_blue",
           "primaryShade": 6},
    children=[
        dcc.Store(id="theme-store", storage_type="local", data="light"),
        app_shell,
    ],
)

if __name__ == "__main__":
    # app.run_server(host="0.0.0.0", port=8080)
    app.run(debug=True)
