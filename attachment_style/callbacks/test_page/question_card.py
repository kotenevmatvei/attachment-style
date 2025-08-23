"""
We need:
    * display questions
    * collect answers
    * show answers when skipping back
    * show submit button after the last question has been visited and leave it there
    *
"""
from dash import callback, Input, Output, State

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
    Input("questions-answered-count-store", "data"),
    State("questions-store", "data"),
)
def update_progress_bar(questions_answered, questions):
    progress_percent = (questions_answered / len(questions)) * 100
    return progress_percent
