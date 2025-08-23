"""
We need:
    * display questions
    * collect answers
    * show answers when skipping back
    * show submit button after the last question has been visited and leave it there
    *
"""
from dash import callback, Input, Output, State

@callback(
    Output("current-item-badge", "children"),
    Input("current-question-count-store", "data"),
    Input("questions-store", "data"),
)
def update_current_item_badge(questions_answered, questions):
    total_items = len(questions)
    return f"Item {questions_answered} from {total_items}"