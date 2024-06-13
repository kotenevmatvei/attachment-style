import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, html

app = Dash(__name__)

app.layout = dmc.MantineProvider(
    dmc.AppShell(
        [
            dmc.AppShellHeader("Header", px=25),
            dmc.AppShellNavbar("Navbar"),
            dmc.AppShellAside("Aside"),
            dmc.AppShellMain(children=[dmc.Text("Hello World")]),
        ],
        header={"height": 70},
        padding="xl",
        zIndex=1400,
        navbar={
            "width": 300,
            "breakpoint": "sm",
            "collapsed": {"mobile": True},
        },
        aside={
            "width": 300,
            "breakpoint": "xl",
            "collapsed": {"desktop": False, "mobile": True},
        },
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)
