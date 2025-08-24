import dash_mantine_components as dmc
from dash import Dash, callback, Input, Output, dcc, State, ctx

import constants

app = Dash(__name__)

app.layout = dmc.MantineProvider(
    dmc.Container(
        children=[
            dcc.Store(id="breakpoints", data={"progress": 1, "current_item": 1}),
            dmc.Space(h=100),
            dmc.Group(
                gap="md",
                children=[
                    dmc.Button("progress forward", id="progress-forward"),
                    dmc.Button("progress backwards", id="progress-backwards"),
                ]
            ),
            dmc.Space(h=50),

            dmc.Paper(
                radius=50,
                shadow="xl",
                children=[
                    dmc.Grid(
                        columns=36,
                        children=[
                            dmc.GridCol(dmc.Paper(" ", h=25, id=str(i), radius="lg", shadow="xl"), span=1)
                            for i in range(1, 37)
                        ],
                        gutter=5,
                        w=900,
                    )
                ]
            ),
        ]
    )
)


@callback(
    [Output(str(i), "bg") for i in range(1, 37)],
    Input("breakpoints", "data")
)
def update_colors(breakpoints):
    colors = {str(i): constants.PRIMARY for i in range(1, breakpoints["progress"] + 1)}
    colors[str(breakpoints["current_item"])] = "red.9"
    full_bar = ([colors[str(i)] for i in range(1, breakpoints["progress"] + 1)]
                + ["gray.0" for i in range(breakpoints["progress"] + 1, 37)])
    return full_bar


@callback(
    Output("breakpoints", "data"),
    [
        Input("progress-forward", "n_clicks"),
        Input("progress-backwards", "n_clicks")
    ],
    State("breakpoints", "data"),
    prevent_inital_call=True,
)
def update_progress(forward_clicks, backwards_clicks, breakpoints):
    triggered_id = ctx.triggered_id
    if triggered_id == "progress-forward":
        if breakpoints["current_item"] == 36:
            return {"current_item": 36, "progress": 36}
        if breakpoints["current_item"] == breakpoints["progress"]:
            return {"current_item": breakpoints["current_item"] + 1, "progress": breakpoints["progress"] + 1}
        else:
            return {"current_item": breakpoints["current_item"] + 1, "progress": breakpoints["progress"]}
    else:
        if breakpoints["current_item"] == 1:
            return {"current_item": 1, "progress": breakpoints["progress"]}
        else:
            return {"current_item": breakpoints["current_item"] - 1, "progress": breakpoints["progress"]}


if __name__ == "__main__":
    app.run(debug=True)
