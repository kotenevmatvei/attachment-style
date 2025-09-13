from dash import callback, Output, Input

@callback(
    [
        Output("current-question-count-store", "data", allow_duplicate=True),
        Output("questions-answered-count-store", "data", allow_duplicate=True),
        Output("answers-store", "data", allow_duplicate=True),
    ],
    [
        Input("url", "pathname")
    ],
    prevent_initial_call=True,
)
def clear_state(pathname):
    return 1, 0, {}
