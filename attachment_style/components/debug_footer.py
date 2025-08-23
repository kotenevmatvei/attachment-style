from dash import callback, Input, Output
import dash_mantine_components as dmc

DebugFooter = dmc.Container(
    w="100%",
    children=[
        dmc.Text(id="subject-debug"),
        dmc.Text(id="questions-debug"),
        dmc.Text(id="demographics-answers-debug"),
    ]
)

@callback(
    Output("subject-debug", "children"),
    Output("questions-debug", "children"),
    Output("demographics-answers-debug", "children"),
    Input("subject-store", "data"),
    Input("questions-store", "data"),
    Input("demographics-answers-store", "data"),
)
def update_debug_text(subject, questions, demographics):
    if all([subject, questions, demographics]):
        return f"subject: {subject}", f"first question: {questions[0]}",f"demographics: {str(demographics[0].values())}"
    elif subject and questions:
        return f"subject: {subject}", f"first question: {questions[0]}", "..."
    else:
        return f"subject: {subject}", "...", "..."
