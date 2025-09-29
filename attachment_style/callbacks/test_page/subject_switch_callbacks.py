from dash import callback, Output, Input, ctx

@callback(
    [
        Output("demographics-questionnaire-collapse", "opened", allow_duplicate=True),
        Output("subject-switch-collapse", "opened")
    ],
    [
        Input("assess-yourself-button", "n_clicks"),
        Input("assess-yourself-button-mobile", "n_clicks"),
        Input("assess-others-button", "n_clicks"),
        Input("assess-others-button-mobile", "n_clicks"),
    ],
    prevent_initial_call=True
)
def toggle_demographics_questionnaire(assess_yourself_click, assess_yourself_mobile_click, assess_others_click, assess_others_mobile_click):
    return True, False

