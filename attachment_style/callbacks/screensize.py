from dash import callback, Input, Output


@callback(
    Output("window-width", "data"),
    Input("breakpoints", "width"),
)
def show_current_breakpoint(window_width: int):
    return window_width


# change page title order on mobile
@callback(
    Output("about-page-title", "order"),
    Input("window-width", "data"),
)
def resize_feedback_page_title(window_width):
    if window_width < 500:
        return 3
    return 1
