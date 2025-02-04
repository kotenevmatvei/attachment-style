from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    ctx,
    callback,
    register_page,
)
from random import shuffle
import copy
import dash_bootstrap_components as dbc
from utils.utils import (
    read_questions,
    calculate_scores,
    build_pie_chart,
    generate_type_description,
    increase_figure_font,
    upload_to_db,
)
from utils.generate_pdf import generate_report

import plotly.io as pio

from components.question_card_others import QuestionCardOthers
from components.results_chart_others import ResultChartOthers
from components.demographics_questionnaire_others import DemographicQuestionnaireOthers

register_page(__name__, path="/asses-others")


def layout(**kwargs):
    return html.Div(
        [
            html.H3("Assess Others", className="text-center"),
            dbc.Collapse(
                DemographicQuestionnaireOthers,
                id="personal-questionnaire-collapse-partner",
                is_open=True,
            ),
            dbc.Collapse(
                [
                    dcc.Markdown(
                        """
                        Please adjust the slider below to evaluate how much you can 
                        relate to the following statements on the scale from 0 to 10.  
                        (e.g. 4 meaning you can agree 40% of the time).  
                        You can use the back and forth buttons to navigate between questions.
                        """,
                        className="text-center",
                    ),
                    QuestionCardOthers,
                ],
                id="question-card-collapse-partner",
                is_open=False,
            ),
            dbc.Collapse(
                dbc.Button("To Results", id="submit-test-button-partner"),
                id="submit-test-collapse-partner",
                is_open=False,
                className="mb-4 text-center",
            ),
            ResultChartOthers,
            # storage
            dcc.Store(
                id="questions-storage-partner",
                data=read_questions("partner"),
                storage_type="memory",
            ),
            dcc.Store(id="question-count-storage-partner", data=0),
            dcc.Store(id="answers-storage-partner", data={}, storage_type="memory"),
            dcc.Store(id="lb-visited-last-storage-partner"),
            dcc.Store(id="last-question-visited-partner", data=False),
            dcc.Store(id="personal-answers-partner"),
            dcc.Interval(id="page-load-interval-partner", interval=1, max_intervals=1),
            # download
            dcc.Download(id="download-report-partner"),
        ]
    )


# submit personal questionnaire
@callback(
    [
        Output("personal-questionnaire-collapse-partner", "is_open"),
        Output("question-card-collapse-partner", "is_open"),
        Output("personal-questionnaire-error-partner", "hidden"),
        Output("personal-answers-partner", "data"),
        Output("personal-questionnaire-error-partner", "children"),
    ],
    Input("submit-personal-questionnaire-partner", "n_clicks"),
    [
        State("age-partner", "value"),
        State("relationship-status-partner", "value"),
        State("gender-partner", "value"),
        State("therapy-experience-partner", "value"),
    ],
)
def sumbmit_personal_questionnaire(
    n_clicks, age, relationship_status, gender, therapy_experience
):
    if n_clicks:
        if all([age, relationship_status, gender, therapy_experience]):
            if age < 0 or age > 100:
                return True, False, False, {}, "Please enter a valid age"
            return (
                False,
                True,
                True,
                {
                    "age": age,
                    "relationship_status": relationship_status,
                    "gender": gender,
                    "therapy_experience": therapy_experience,
                },
                "",
            )
        else:
            return True, False, False, {}, "Please fill out all fields before contnuing"
    return True, False, True, {}, ""


# shuffle questions on page load
@callback(
    [
        Output("questions-storage-partner", "data"),
        Output("question-text-partner", "children", allow_duplicate=True),
    ],
    Input("page-load-interval-partner", "n_intervals"),
    State("questions-storage-partner", "data"),
    prevent_initial_call=True,
)
def shuffle_questions(n, questions):
    shuffle(questions)
    return questions, questions[0][0]


# show submit button after last question visited
@callback(
    Output("submit-test-collapse-partner", "is_open"),
    Input("last-question-visited-partner", "data"),
)
def show_submit_button(last_question_visited: bool) -> bool:
    return last_question_visited


# Submit test
@callback(
    [
        Output("dashboard-collapse-partner", "is_open"),
        Output("pie-chart-partner", "figure"),
        Output("type-description-markdown-partner", "children"),
    ],
    Input("submit-test-button-partner", "n_clicks"),
    [
        State("answers-storage-partner", "data"),
        State("question-count-storage-partner", "data"),
        State("questions-storage-partner", "data"),
        State("slider-partner", "value"),
        State("personal-answers-partner", "data"),
    ],
    prevent_initial_call=True,
)
def generate_dashboard(
    n_clicks, answers, question_count, questions, slider_value, personal_answers
):
    if question_count == len(questions):
        answers[f"{question_count-1}"] = (
            questions[question_count - 1][1],
            slider_value,
            questions[question_count - 1][0],
        )
    # load to db
    if n_clicks == 1:  # only save on the first click
        upload_to_db(answers, personal_answers)
    if n_clicks:
        (anxious_score, secure_score, avoidant_score) = calculate_scores(answers)
        if anxious_score >= secure_score and anxious_score >= avoidant_score:
            description = generate_type_description("anxious")
        if secure_score >= avoidant_score and secure_score >= anxious_score:
            description = generate_type_description("secure")
        if avoidant_score >= secure_score and avoidant_score >= anxious_score:
            description = generate_type_description("avoidant")

        fig = build_pie_chart(
            anxious_score=anxious_score,
            secure_score=secure_score,
            avoidant_score=avoidant_score,
        )

        fig_to_download = copy.deepcopy(fig)
        increase_figure_font(fig_to_download)

        pio.write_image(
            fig_to_download, "tmp/figure.png", width=700 * 1.5, height=500 * 1.5
        )
        return True, fig, description


# Dwnload report
@callback(
    Output("download-report-partner", "data"),
    Input("download-report-button-partner", "n_clicks"),
    State("answers-storage-partner", "data"),
    prevent_initial_call=True,
)
def load_report(n_clicks, answers):
    if n_clicks:
        generate_report(answers)
        return dcc.send_file("tmp/attachment_style_report.pdf", type="pdf")


@callback(
    [
        Output("question-count-storage-partner", "data"),
        Output("question-count-text-partner", "children"),
        Output("question-text-partner", "children"),
        Output("answers-storage-partner", "data"),
        Output("slider-partner", "value"),
        Output("lb-visited-last-storage-partner", "data"),
        Output("last-question-visited-partner", "data"),
    ],
    [
        Input("right-button-partner", "n_clicks"),
        Input("left-button-partner", "n_clicks"),
    ],
    [
        State("slider-partner", "value"),
        State("question-count-storage-partner", "data"),
        State("questions-storage-partner", "data"),
        State("answers-storage-partner", "data"),
        State("lb-visited-last-storage-partner", "data"),
        State("last-question-visited-partner", "data"),
    ],
)
def update_question(
    r_clicks: int,
    l_clicks: int,
    slider_value: float,
    question_count: int,
    questions: list[tuple[str, str]],
    answers: dict[str, tuple[str, float, str]],
    lb_visited_last: bool,
    last_question_visited: bool,
):
    n: int = len(questions)
    id_triggered = ctx.triggered_id
    if not last_question_visited:
        match id_triggered:
            case "right-button-partner":
                answers[f"{question_count-1}"] = (
                    questions[question_count - 1][1],
                    slider_value,
                    questions[question_count - 1][0],
                )
                # questions between first and one before last one
                if question_count < n - 1:
                    question_count += 1
                    if f"{question_count-1}" in answers.keys():
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            answers[f"{question_count-1}"][1],
                            False,
                            False,
                        )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            0,
                            False,
                            False,
                        )
                # question before last one (show submit button next)
                elif question_count == n - 1:
                    question_count += 1
                    if f"{question_count-1}" in answers.keys():
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            answers[f"{question_count-1}"][1],
                            False,
                            True,
                        )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            0,
                            False,
                            True,
                        )
                # last question
                else:
                    return (
                        question_count,
                        f"Question {n}/{n}",
                        questions[n - 1][0],
                        answers,
                        answers[f"{question_count-1}"][1],
                        False,
                        True,
                    )

            case "left-button-partner":
                if question_count == 1:
                    answers["0"] = (
                        questions[0][1],
                        slider_value,
                        questions[question_count - 1][0],
                    )
                    return (
                        1,
                        f"Question 1/{n}",
                        questions[0][0],
                        answers,
                        answers["0"][1],
                        True,
                        False,
                    )
                else:
                    answers[f"{question_count-1}"] = (
                        questions[question_count - 1][1],
                        slider_value,
                        questions[question_count - 1][0],
                    )
                    return (
                        question_count - 1,
                        f"Question {question_count-1}/{n}",
                        questions[question_count - 2][0],
                        answers,
                        answers[f"{question_count - 2}"][1],
                        True,
                        False,
                    )

    else:
        match id_triggered:
            case "right-button-partner":
                # questions between first and last
                if question_count < n:
                    answers[f"{question_count - 1}"] = (
                        questions[question_count - 1][1],
                        slider_value,
                        questions[question_count - 1][0],
                    )
                    question_count += 1
                    if f"{question_count-1}" in answers.keys():
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            answers[f"{question_count - 1}"][1],
                            False,
                            True,
                        )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            0,
                            False,
                            True,
                        )
                # last question
                else:
                    answers[f"{question_count - 1}"] = (
                        questions[question_count - 1][1],
                        slider_value,
                        questions[question_count - 1][0],
                    )
                    return (
                        question_count,
                        f"Question {n}/{n}",
                        questions[n - 1][0],
                        answers,
                        answers[f"{question_count - 1}"][1],
                        False,
                        True,
                    )

            case "slider-partner":
                # questions between first and last
                if question_count < n:
                    answers[f"{question_count - 1}"] = (
                        questions[question_count - 1][1],
                        slider_value,
                        questions[question_count - 1][0],
                    )
                    if not lb_visited_last:
                        question_count += 1
                        if f"{question_count-1}" in answers.keys():
                            return (
                                question_count,
                                f"Question {question_count}/{n}",
                                questions[question_count - 1][0],
                                answers,
                                answers[f"{question_count - 1}"][1],
                                False,
                                True,
                            )
                        else:
                            return (
                                question_count,
                                f"Question {question_count}/{n}",
                                questions[question_count - 1][0],
                                answers,
                                0,
                                False,
                                True,
                            )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            answers[f"{question_count - 1}"][1],
                            False,
                            True,
                        )
                # last question
                else:
                    answers[f"{question_count - 1}"] = (
                        questions[question_count - 1][1],
                        slider_value,
                        questions[question_count - 1][0],
                    )
                    return (
                        question_count,
                        f"Question {n}/{n}",
                        questions[n - 1][0],
                        answers,
                        answers[f"{question_count - 1}"][1],
                        False,
                        True,
                    )

            case "left-button-partner":
                if question_count == 1:
                    answers["0"] = (questions[0][1], slider_value)
                    return (
                        1,
                        f"Question 1/{n}",
                        questions[0][0],
                        answers,
                        answers["0"][1],
                        True,
                        True,
                    )
                else:
                    answers[f"{question_count - 1}"] = (
                        questions[question_count - 1][1],
                        slider_value,
                        questions[question_count - 1][0],
                    )
                    return (
                        question_count - 1,
                        f"Question {question_count - 1}/{n}",
                        questions[question_count - 2][0],
                        answers,
                        answers[f"{question_count - 2}"][1],
                        True,
                        True,
                    )

    # first question / initial state
    return (1, f"Question {1}/{n}", questions[0][0], answers, 0, False, False)
