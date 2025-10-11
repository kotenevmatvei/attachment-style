from dash import callback, Input, Output


@callback(
    Output("window-width", "data"),
    Input("breakpoints", "width"),
)
def show_current_breakpoint(window_width: int):
    return window_width

