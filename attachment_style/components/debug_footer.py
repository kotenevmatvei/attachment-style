import dash_mantine_components as dmc
from dash import callback, Input, Output

DebugFooter = dmc.Container(
    w="100%",
    children=[
        dmc.Button(
            "show debug footer",
            id="show-debug-footer-button",
            size="sm",
            n_clicks=0,
        ),
        dmc.Container(
            id="debug-container",
            children=[
                dmc.Text(id="subject-debug"),
                dmc.Text(id="questions-debug"),
                dmc.Text(id="demographics-answers-debug"),
                dmc.Text(id="answers-debug"),
            ]
        )
    ]
)


@callback(
    Output("subject-debug", "children"),
    Output("demographics-answers-debug", "children"),
    Output("questions-debug", "children"),
    Output("answers-debug", "children"),
    Input("subject-store", "data"),
    Input("demographics-answers-store", "data"),
    Input("questions-store", "data"),
    Input("answers-store", "data"),
)
def update_debug_text(subject, demographics, questions, answers):
    return f"subject: {subject}\n", f"demographics: {str(demographics)}", f"questions: {str(questions)}", f"answers: {str(answers)}"


@callback(
    Output("debug-container", "style"),
    Input("show-debug-footer-button", "n_clicks")
)
def toggle_debug_footer(n_clicks):
    if n_clicks % 2:
        return {"display": "block"}
    else:
        return {"display": "none"}