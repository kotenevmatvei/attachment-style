"""
We need:
    * display questions
    * collect answers
    * show answers when skipping back
    * show submit button after the last question has been visited and leave it there
    *
"""
import logging

import dash_mantine_components as dmc
from dash import callback, Input, Output, State, ctx, ALL
from dash.exceptions import PreventUpdate

import constants
from utils.utils import revert_scores_for_reverted_questions, calculate_scores

logger = logging.getLogger(__name__)


# current item badge
@callback(
    Output("current-item-badge", "children"),
    [
        Input("current-question-count-store", "data"),
        Input("questions-store", "data"),
    ]
)
def update_current_item_badge(current_question, questions):
    total_items = len(questions)
    return f"Item {current_question} from {total_items}"


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
    + [Input(f"option-{i}", "n_clicks") for i in range(1, 8)],
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

    # ignore hydration/refresh triggers where the input value is None or 0
    if not ctx.triggered or ctx.triggered[0].get("value") in (None, 0):
        raise PreventUpdate

    # --------- click on one of the options -----------
    if triggered_id in [f"option-{i}" for i in range(1, 8)]:
        # get the value in any case
        value = int(triggered_id.split("-")[1])

        # old value for loggin / debugging
        if answers[str(current_question_count)]:
            old_value = answers[str(current_question_count)][1]
            # logger.info(f"already been here. your old value: {old_value}")
            # logger.info("Navigation case 1")

        answers[str(current_question_count)] = (
            questions[current_question_count - 1][1], value, questions[current_question_count - 1][0]
        )
        # logger.info(f"your new value: {answers[str(current_question_count)][1]}")

        # at the last question
        if current_question_count == questions_len:
            # has it already been answered? -> don't update questions_answered_count
            if questions_answered_count == questions_len:
                # logger.info("Navigation case 2")
                return current_question_count, questions_answered_count, answers, False, False, True, True
            # update question_count (should become eq. questions_len now)
            else:
                # logger.info("Navigation case 3")
                return current_question_count, questions_answered_count + 1, answers, False, False, True, True
        # we are returning (rewriting, since clicking on the answer options, not navigation btns) after skipping back
        # but we have not yet reached the last answered question, so forward buttons enabled
        elif current_question_count < questions_answered_count:
            # check if next comes the last question!
            if current_question_count == questions_len - 1:
                return current_question_count + 1, questions_answered_count, answers, False, False, True, True
            # logger.info("Navigation case 4")
            return current_question_count + 1, questions_answered_count, answers, False, False, False, False
        # we have reached the last answered question - block the forward buttons for the next one (new!)
        elif current_question_count == questions_answered_count:
            # logger.info("Navigation case 5")
            return current_question_count + 1, questions_answered_count, answers, False, False, True, True
        # we are answering a new question
        elif current_question_count == questions_answered_count + 1:
            # logger.info("Navigation case 6")
            return current_question_count + 1, questions_answered_count + 1, answers, False, False, True, True

    # ---------- skipping through questions via navigation buttons ------------
    # moving forward
    if triggered_id in ["forward-button", "next-button"]:
        # check if next comes the last question!
        if current_question_count == questions_len - 1:
            return current_question_count + 1, questions_answered_count, answers, False, False, True, True
        # disable the forward buttons if the next question is the last onw the user had answered
        if current_question_count == questions_answered_count:
            # logger.info("Navigation case 7")
            return current_question_count + 1, questions_answered_count, answers, False, False, True, True
        else:
            # logger.info("Navigation case 8")
            return current_question_count + 1, questions_answered_count, answers, False, False, False, False

    # moving backwards
    if triggered_id in ["back-button", "prev-button"]:
        # we have reached the beginning ------> ah this state is impossible to reach :)
        # if current_question_count == 1:
        #     logger.info("Navigation case 9")
        #     return current_question_count, questions_answered_count, answers, True, True, False, False
        # block the back buttons already if next comes the first question
        if current_question_count == 2:
            # logger.info("Navigation case 10")
            return current_question_count - 1, questions_answered_count, answers, True, True, False, False
        else:
            # logger.info("Navigation case 11")
            return current_question_count - 1, questions_answered_count, answers, False, False, False, False

    # logger.info("Navigation case 0")
    return 1, 0, answers, True, True, True, True


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


# enable the to-results button only after the last question has been answered
@callback(
    Output("to-results-button", "disabled"),
    Input("questions-answered-count-store", "data"),
    State("questions-len", "data")
)
def enable_to_results_button(questions_answered_count, questions_len):
    if questions_answered_count == questions_len:
        return False
    return True



@callback(
    [
        Output("results-board-collapse", "opened"),
        Output("question-card-collapse", "opened", allow_duplicate=True),
        Output("result-scores-store", "data"),
    ],
    Input("to-results-button", "n_clicks"),
    State("answers-store", "data"),
    prevent_initial_call=True,
)
def toggle_results_collapse(to_results_click, answers):
    if to_results_click:
        reverted_answers = revert_scores_for_reverted_questions(answers)
        anxious_score, secure_score, avoidant_score = calculate_scores(reverted_answers)
        result_scores = {"anxious_score": anxious_score, "secure_score": secure_score, "avoidant_score": avoidant_score}
        return True, False, result_scores

    # start with 1's to avoid dividing by 0
    return False, True, {"anxious_score": 1, "avoidant_score": 0, "secure_score": 0}
