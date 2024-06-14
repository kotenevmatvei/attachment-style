import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, html

app = Dash(__name__)

app.layout = dmc.MantineProvider(
    dmc.AppShell(
        [
            dmc.AppShellHeader("Header"),
            dmc.AppShellMain("Main"),
            dmc.AppShellFooter("Footer")
        ],
        header={
            "height": 70,
        },
        footer={
            "height": 70
        }
    )
)

if __name__ == "__main__":
    app.run_server(debug=True)
