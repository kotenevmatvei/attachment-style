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
        Output("current-question-count-store", "data"),
        Output("questions-answered-count-store", "data"),
        Output("answers-store", "data"),
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
    + [Input(f"option-{i}", "c_clicks") for i in range(7)],
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

    # if triggered_id in [f"option-{i}" for i in range(7)]:
    #     match triggered_id:
    #         case "option-1":
    #             answers[str(current_question_count)] = (
    #                 questions[current_question_count][1], 1, questions[current_question_count][0]
    #             )

    if triggered_id in ["forward-button", "next-button"]:
        if current_question_count == questions_len:
            return current_question_count, questions_answered_count
        elif current_question_count == questions_answered_count:
            return current_question_count + 1, questions_answered_count + 1
        else:
            return current_question_count + 1, questions_answered_count

    if triggered_id in ["back-button", "prev-button"]:
        if current_question_count == 1:
            return current_question_count, questions_answered_count
        else:
            return current_question_count - 1, questions_answered_count

    return 1, 1


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
    + [Output(f"option-{i}", "bg") for i in range(7)]
    + [Output(f"option-{i}", "c") for i in range(7)],
    Input("mantine-provider", "forceColorScheme"),
)
def update_question_card_style(theme):
    if theme == "dark":
        return (
            {"backgroundColor": dmc.DEFAULT_THEME["colors"]["dark"][6]},
            *["dark" for i in range(7)],
            *["white" for i in range(7)]
            # *[dmc.DEFAULT_THEME["colors"]["dark"][7] for i in range(7)]
        )
    else:
        return (
            {"backgroundColor": dmc.DEFAULT_THEME["colors"]["gray"][1]},
            *["gray.1" for i in range(7)],
            *["black" for i in range(7)]
            # *[dmc.DEFAULT_THEME["colors"]["dark"][1] for i in range(7)]
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
