from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    ctx,
    callback,
    register_page,
    clientside_callback,
)
from random import shuffle
import copy
import logging
import dash_bootstrap_components as dbc
from utils.utils import (
    read_questions,
    calculate_scores,
    build_pie_chart,
    retrieve_scores_from_db,
    revert_questions,
    generate_type_description,
    increase_figure_font,
    upload_to_db,
)
from utils.generate_pdf import generate_report

import plotly.io as pio

from components.question_card_others import QuestionCardOthers
from components.results_chart_others import ResultChartOthers
from components.demographics_questionnaire_others import DemographicQuestionnaireOthers

logger = logging.getLogger(__name__)
register_page(__name__, path="/asses-others")


def layout(**kwargs):
    return html.Div(
        [
            html.Div(id="dummy-for-keydown-others"),
            html.Div(id="dummy-div-pic-download-others"),
            html.H3("Assess Others", className="text-center"),
            dbc.Collapse(
                DemographicQuestionnaireOthers,
                id="personal-questionnaire-collapse-others",
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
                id="question-card-collapse-others",
                is_open=False,
            ),
            dbc.Collapse(
                dbc.Button("To Results", id="submit-test-button-others"),
                id="submit-test-collapse-others",
                is_open=False,
                className="mb-4 text-center",
            ),
            ResultChartOthers,
            # storage
            dcc.Store(
                id="questions-storage-others",
                data=read_questions("others"),
                storage_type="memory",
            ),
            dcc.Store(id="question-count-storage-others", data=0),
            dcc.Store(id="answers-storage-others", data={}, storage_type="memory"),
            dcc.Store(id="lb-visited-last-storage-others"),
            dcc.Store(id="last-question-visited-others", data=False),
            dcc.Store(id="personal-answers-others"),
            dcc.Store(id="figure-store-others"),
            dcc.Interval(id="page-load-interval-others", interval=1, max_intervals=1),
            # download
            dcc.Download(id="download-report-others"),
        ]
    )


# submit personal questionnaire
@callback(
    [
        Output("personal-questionnaire-collapse-others", "is_open"),
        Output("question-card-collapse-others", "is_open"),
        Output("personal-questionnaire-error-others", "hidden"),
        Output("personal-answers-others", "data"),
        Output("personal-questionnaire-error-others", "children"),
    ],
    Input("submit-personal-questionnaire-others", "n_clicks"),
    [
        State("age-others", "value"),
        State("relationship-status-others", "value"),
        State("gender-others", "value"),
        State("therapy-experience-others", "value"),
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


# shuffle questions on page load -- comment out when testing!
@callback(
    [
        Output("questions-storage-others", "data"),
        Output("question-text-others", "children", allow_duplicate=True),
    ],
    Input("page-load-interval-others", "n_intervals"),
    State("questions-storage-others", "data"),
    prevent_initial_call=True,
)
def shuffle_questions(n, questions):
    shuffle(questions)
    return questions, questions[0][0]


# show submit button after last question visited
@callback(
    Output("submit-test-collapse-others", "is_open"),
    Input("last-question-visited-others", "data"),
)
def show_submit_button(last_question_visited: bool) -> bool:
    return last_question_visited


# Submit test
@callback(
    [
        Output("dashboard-collapse-others", "is_open"),
        Output("pie-chart-others", "figure"),
        Output("type-description-markdown-others", "children"),
        Output("figure-store-others", "data")
    ],
    Input("submit-test-button-others", "n_clicks"),
    [
        State("answers-storage-others", "data"),
        State("question-count-storage-others", "data"),
        State("questions-storage-others", "data"),
        State("slider-others", "value"),
        State("personal-answers-others", "data"),
    ],
    prevent_initial_call=True,
)
def generate_dashboard(
    n_clicks, answers, question_count, questions, slider_value, personal_answers
):
    logger.info("Begin generating the dashboard...")
    if question_count == len(questions):
        answers[f"{question_count - 1}"] = (
            questions[question_count - 1][1],
            slider_value,
            questions[question_count - 1][0],
        )
    if n_clicks:
        if n_clicks == 1:
            # upload to db the first time
            logger.info("Started uploading to db...")
            upload_to_db(answers, personal_answers, test=False)
            logger.info("Finished uploading to db")
        (anxious_score, secure_score, avoidant_score) = calculate_scores(answers)

        if anxious_score >= secure_score and anxious_score >= avoidant_score:
            description = generate_type_description("anxious")
        if secure_score >= avoidant_score and secure_score >= anxious_score:
            description = generate_type_description("secure")
        if avoidant_score >= secure_score and avoidant_score >= anxious_score:
            description = generate_type_description("avoidant")

        logger.info("Building the ecr_r chart for browser...")

        fig = build_pie_chart(
            anxious_score=anxious_score,
            secure_score=secure_score,
            avoidant_score=avoidant_score,
        )

        logger.info("Done building the ecr_r chart for browser...")
        logger.info("Converting the plot to json...")
        fig_json = fig.to_json()

        # print(fig_dict)

        ### this is for testing ###
        # with open("tests/app_scores_before_revert.csv", "a") as f:
        #     writer = csv.writer(f)
        #     writer.writerow(scores_before_revert)

        # with open("tests/app_scores_after_revert.csv", "a") as f:
        #     writer = csv.writer(f)
        #     writer.writerow(scores_after_revert)

        # with open("tests/app_averages.csv", "a") as f:
        #     writer = csv.writer(f)
        #     row = [round(anxious_score, 2), round(avoidant_score, 2)]
        #     writer.writerow(row)

        return True, fig, description, fig_json

@callback(
    Output("dummy-div-pic-download-others", "style"),
    Input("figure-store-others", "data"),
    prevent_initial_call=True,
)
def download_plot_picture(fig_json):
    
    fig = pio.from_json(fig_json)

    logger.info("Saving the image...")
    pio.write_image(
        fig, "tmp/figure.png", width=700, height=500
    )
    logger.info("Image saved")
    
    return {}

# Dwnload report
@callback(
    Output("download-report-others", "data"),
    Input("download-report-button-others", "n_clicks"),
    State("answers-storage-others", "data"),
    prevent_initial_call=True,
)
def load_report(n_clicks, answers):
    if n_clicks:
        generate_report(answers)
        return dcc.send_file("tmp/attachment_style_report.pdf", type="pdf")


@callback(
    [
        Output("question-count-storage-others", "data"),
        Output("question-count-text-others", "children"),
        Output("question-text-others", "children"),
        Output("answers-storage-others", "data"),
        Output("slider-others", "value"),
        Output("lb-visited-last-storage-others", "data"),
        Output("last-question-visited-others", "data"),
    ],
    [
        Input("right-button-others", "n_clicks"),
        Input("left-button-others", "n_clicks"),
    ],
    [
        State("slider-others", "value"),
        State("question-count-storage-others", "data"),
        State("questions-storage-others", "data"),
        State("answers-storage-others", "data"),
        State("lb-visited-last-storage-others", "data"),
        State("last-question-visited-others", "data"),
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
            case "right-button-others":
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
                            1,
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
                            1,
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

            case "left-button-others":
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
            case "right-button-others":
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
                            1,
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

            case "slider-others":
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
                                1,
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

            case "left-button-others":
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
    return (1, f"Question {1}/{n}", questions[0][0], answers, 1, False, False)


clientside_callback(
    """
    function(trigger) {
        if (!window.arrowKeysListenerAttached) {
            function ArrowClick(event) {
                if (event.key === "ArrowRight") {
                    document.getElementById('right-button-others').click();
                } else if (event.key === "ArrowLeft") {
                    document.getElementById('left-button-others').click();
                }
            }
            
            window.addEventListener('keydown', ArrowClick);
            window.arrowKeysListenerAttached = true; 
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("dummy-for-keydown-others", "style"),
    Input("dummy-for-keydown-others", "style"),
)

