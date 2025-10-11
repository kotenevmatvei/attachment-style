from dash import callback, Input, Output


@callback(
    Output("window-width", "data"),
    Input("breakpoints", "width"),
)
def show_current_breakpoint(window_width: int):
    return window_width


@callback(
    Output("screen-size-text", "children"),
    Input("window-width", "data")
)
def display_screen_size(window_width):
    return str(window_width)
