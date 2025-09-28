from dash import Output, Input, callback, ctx

@callback(
    Output("test-stepper", "active"),
    [
        Input("subject-switch-collapse", "opened"),
        Input("demographics-questionnaire-collapse", "opened"),
        Input("question-card-collapse", "opened"),
        Input("results-board-collapse", "opened"),
        Input("download-report-button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def update_steper(subject_opened, demographics_opened, questions_opened, results_opened, download_report_btn):
    button_id = ctx.triggered_id
    if button_id == "download-report-button":
        return 4
    if subject_opened:
        return 0
    elif demographics_opened:
        return 1
    elif questions_opened:
        return 2
    elif results_opened:
        return 3

    return 0


@callback(
    Output("test-stepper-mobile", "active"),
    [
        Input("subject-switch-collapse", "opened"),
        Input("demographics-questionnaire-collapse", "opened"),
        Input("question-card-collapse", "opened"),
        Input("results-board-collapse", "opened"),
        Input("download-report-button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def update_steper(subject_opened, demographics_opened, questions_opened, results_opened, download_report_btn):
    button_id = ctx.triggered_id
    if button_id == "download-report-button":
        return 4
    if subject_opened:
        return 0
    elif demographics_opened:
        return 1
    elif questions_opened:
        return 2
    elif results_opened:
        return 3

    return 0
