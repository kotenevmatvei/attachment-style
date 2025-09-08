from dash import callback, Output, Input

@callback(
    [
        Output("current-question-count-store", "data", allow_duplicate=True),
        Output("questions-answered-count-store", "data", allow_duplicate=True),
        Output("answers-store", "data", allow_duplicate=True),
        Output("subject-switch-collapse", "opened", allow_duplicate=True),
        Output("demographics-questionnaire-collapse", "opened", allow_duplicate=True),
        Output("question-card-collapse", "opened", allow_duplicate=True),
        Output("results-board-collapse", "opened", allow_duplicate=True),
    ],
    [
        Input("logo-div", "n_clicks"),
        Input("test-anchor-header", "n_clicks"),
        Input("retake-survey-button", "n_clicks")
    ],
    prevent_initial_call=True,
)
def clear_state(logo_clicks, test_anchor_clicks, retake_survey_clicks):
    return 1, 0, {}, True, False, False, False