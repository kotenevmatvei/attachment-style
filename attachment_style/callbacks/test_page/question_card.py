"""
We need:
    * display questions
    * collect answers
    * show answers when skipping back
    * show submit button after the last question has been visited and leave it there
    *
"""
import dash_mantine_components as dmc
from dash import callback, Input, Output, State, ctx, ALL
from dash.exceptions import PreventUpdate

import constants


# current item badge
@callback(
    Output("current-item-badge", "children"),
    Input("current-question-count-store", "data"),
    State("questions-store", "data"),
)
def update_current_item_badge(questions_answered, questions):
    total_items = len(questions)
    return f"Item {questions_answered} from {total_items}"


# display question
@callback(
    Output("question-markdown", "children"),
    [
        Input("current-question-count-store", "data"),
        Input("questions-store", "data"),
    ],
    State("subject-store", "data"),
)
def display_question(current_question_count, questions, subject):
    question_ind = current_question_count - 1
    question_text = questions[question_ind][0]
    return question_text


# update question (a.k.a. the killer)
@callback(
    [
        # state
        Output("current-question-count-store", "data"),
        Output("questions-answered-count-store", "data"),
        Output("answers-store", "data"),

        # navigation buttons disables?
        Output("back-button", "disabled"),
        Output("prev-button", "disabled"),
        Output("forward-button", "disabled"),
        Output("next-button", "disabled"),
    ],
    [
        # forward
        Input("forward-button", "n_clicks"),
        Input("next-button", "n_clicks"),
        # backwards
        Input("back-button", "n_clicks"),
        Input("prev-button", "n_clicks"),
    ]
    # answer option buttons
    + [Input(f"option-{i}", "n_clicks") for i in range(1,8)],
    [
        State("current-question-count-store", "data"),
        State("questions-len", "data"),
        State("questions-store", "data"),
        State("questions-answered-count-store", "data"),
        State("answers-store", "data"),
    ],
    prevent_initial_call=True,
)
def update_question(
        # navigation buttons
        forward_clicks, next_clicks, back_clicks, prev_clicks,

        # answer option buttons
        str_dis_click, dis_click, sl_dis_click, neu_click,
        sl_ag_click, ag_click, str_ag_click,

        # state
        current_question_count, questions_len, questions,
        questions_answered_count, answers
):
    """
    Update the question, the progress, and the answers. Answers are stored in a dictionary
    with the following structure:
    {"question-ind": ("attachment-style", value, "question-text"), "question-ind+1": (...), ...}
    We are storing the corresponding attachment style because the questions are shuffled.
    """

    triggered_id = ctx.triggered_id

    # Ignore hydration/refresh triggers where the input value is None or 0
    if not ctx.triggered or ctx.triggered[0].get("value") in (None, 0):
        raise PreventUpdate

    print("triggered id: ", triggered_id)

    # --------- click on one of the options -----------
    if triggered_id in [f"option-{i}" for i in range(1,8)]:
        # get the value in any case
        value = int(triggered_id.split("-")[1])
        answers[str(current_question_count)] = (
            questions[current_question_count - 1][1], value, questions[current_question_count - 1][0]
        )
        # we have reached the end
        if current_question_count == questions_len:
            return current_question_count, questions_answered_count, answers, False, False, True, True
        # we are returning (rewriting, since clicking on the answer options, not navigation btns) after skipping back
        elif current_question_count < questions_answered_count - 1:
            return current_question_count + 1, questions_answered_count, answers, False, False, False, False
        # we are moving to a new question
        else:
            return current_question_count + 1, questions_answered_count + 1, answers, False, False, True, True

    # ---------- skipping through questions via navigation buttons ------------
    # moving forward
    if triggered_id in ["forward-button", "next-button"]:
        # disable the forward buttons if the next question is the last the useer had answered
        if current_question_count == questions_answered_count - 1:
            return current_question_count + 1, questions_answered_count, answers, False, False, True, True
        else:
            return current_question_count + 1, questions_answered_count, answers, False, False, False, False

    # moving backwards
    if triggered_id in ["back-button", "prev-button"]:
        # we have reached the beginning
        if current_question_count == 1:
            return current_question_count, questions_answered_count, answers, True, True, False, False
        # block the back buttons already if next comes the first question
        elif current_question_count == 2:
            return current_question_count, questions_answered_count, answers, True, True, False, False
        else:
            return current_question_count - 1, questions_answered_count, answers, False, False, False, False

    return 1, 1, answers, True, True, True, True


# color the step indicators
@callback(
    Output({"type": "question-indicator", "index": ALL}, "bg"),
    [
        Input("questions-answered-count-store", "data"),
        Input("current-question-count-store", "data"),
        Input("questions-len", "data"),
        Input("mantine-provider", "forceColorScheme"),
    ]
)
def update_colors(progress, current_question, questions_len, theme):
    n = questions_len
    colors = []
    for i in range(1, n + 1):
        if i == current_question:
            colors.append("red.9")
        elif i <= progress:
            colors.append(constants.PRIMARY)
        else:
            if theme == "light":
                colors.append("indigo.0")
            else:
                colors.append("gray")
    return colors


# style depending on the theme
@callback(
    [Output("question-paper", "style")]
    + [Output(f"option-{i}", "bg") for i in range(1,8)]
    + [Output(f"option-{i}", "c") for i in range(1,8)],
    Input("mantine-provider", "forceColorScheme"),
)
def update_question_card_style(theme):
    if theme == "dark":
        return (
            {"backgroundColor": dmc.DEFAULT_THEME["colors"]["dark"][6]},
            *["dark" for i in range(1,8)],
            *["white" for i in range(1,8)]
            # *[dmc.DEFAULT_THEME["colors"]["dark"][7] for i in range(1,8)]
        )
    else:
        return (
            {"backgroundColor": dmc.DEFAULT_THEME["colors"]["gray"][1]},
            *["gray.1" for i in range(1,8)],
            *["black" for i in range(1,8)]
            # *[dmc.DEFAULT_THEME["colors"]["dark"][1] for i in range(1,8)]
        )


@callback(
    [
        Output("results-board-collapse", "opened"),
        Output("question-card-collapse", "opened", allow_duplicate=True),
    ],
    [
        Input("to-results-button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def toggle_results_collapse(to_results_click):
    if to_results_click:
        return True, False
    return False, True
