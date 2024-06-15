import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, html

app = Dash(__name__)

app.layout = dmc.MantineProvider(
    dmc.AppShell(
        [
            dmc.AppShellHeader(
                # dmc.Title(
                #     "Attachment Style Test",
                #     styles={"align": "center"},
                # )
                dmc.Grid(
                    children=[
                        dmc.GridCol(
                            dmc.Title(
                                "Attachment Style Test",
                                ta="center",
                                mt=5,
                            ),
                            span=4,
                            offset=4
                        ),
                        dmc.GridCol(
                            dmc.Button(
                                "Language",
                                ta="center",
                                mt=10
                            ),
                            span=1,
                            offset=2
                        )
                    ],
                    # justify="center",
                    # styles={
                    #     "justify-content": "center"
                    # }
                ),
            ),
            dmc.AppShellMain(
                dmc.Center(
                    dmc.Card("Am I at the center?")
                )
            ),
            dmc.AppShellFooter("Footer")
        ],
        header={
            "height": 60,
        },
        footer={
            "height": 60
        }
    )
)

if __name__ == "__main__":
    app.run_server(debug=True)
