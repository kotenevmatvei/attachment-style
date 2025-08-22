from dash import callback, Input, Output, ctx

@callback(
    Output("subject-store", "data"),
    [
        Input("assess-yourself-button", "n_clicks"),
        Input("assess-others-button", "n_clicks"),
    ]
)
def update_subject_store(assess_yourself_click, assess_others_click):
    triggered_id = ctx.triggered_id
    if triggered_id == "assess-others-button":
        return "others"
    return "yourself"

@callback(
    Output("current-subject", "children"),
    Input("subject-store", "data"),
)
def update_current_subject(subject):
    return subject