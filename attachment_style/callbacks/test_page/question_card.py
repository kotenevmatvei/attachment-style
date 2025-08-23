"""
We need:
    * display questions
    * collect answers
    * show answers when skipping back
    * show submit button after the last question has been visited and leave it there
    *
"""
import dash_mantine_components as dmc
from dash import callback, Input, Output, State, dcc


# current item badge
@callback(
    Output("current-item-badge", "children"),
    Input("current-question-count-store", "data"),
    State("questions-store", "data"),
)
def update_current_item_badge(questions_answered, questions):
    total_items = len(questions)
    return f"Item {questions_answered} from {total_items}"


# progress bar
@callback(
    Output("progress-bar", "value"),

    [
        Input("questions-answered-count-store", "data"),
        Input("questions-store", "data"),
    ]
)
def update_progress_bar(questions_answered, questions):
    progress_percent = (questions_answered / len(questions)) * 100
    return progress_percent


# question paper
@callback(
    Output("question-paper", "children"),
    [
        Input("current-question-count-store", "data"),
        Input("questions-store", "data"),
    ],
    State("subject-store", "data"),
)
def update_question_paper(current_question_count, questions, subject):
    question_ind = current_question_count - 1
    align = "center" if subject == "you" else "left"
    question_text = dcc.Markdown(questions[question_ind][0], style={"textAlign": align})
    return question_text


# style question paper
@callback(
    Output("question-paper", "style"),
    Input("mantine-provider", "forceColorScheme"),
)
def update_question_card_style(theme):
    if theme == "dark":
        return {"backgroundColor": dmc.DEFAULT_THEME["colors"]["dark"][6]}
    else:
        return {"backgroundColor": dmc.DEFAULT_THEME["colors"]["gray"][1]}
