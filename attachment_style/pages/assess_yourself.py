from dash import (
    clientside_callback,
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
import plotly.io as pio
import dash_bootstrap_components as dbc

from components.question_card import QuestionCard
from components.results_chart import ResultsChart
from components.demographics_questionnaire import DemographicsQuestionnaire

from utils.utils import (
    build_ecr_r_chart,
    read_questions,
    calculate_scores,
    build_pie_chart,
    generate_type_description,
    increase_figure_font,
    revert_questions,
    upload_to_db,
)
from utils.generate_pdf import generate_report

register_page(__name__, path="/assess-yourself")


def layout(**kwargs):
    return html.Div(
        [
            html.Div(id="dummy-for-keydown"),
            html.H3("Assess Yourself", className="text-center"),
            dbc.Collapse(
                DemographicsQuestionnaire,
                id="personal-questionnaire-collapse",
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
                    QuestionCard,
                ],
                id="question-card-collapse",
                is_open=False,
            ),
            dbc.Collapse(
                dbc.Button("To Results", id="submit-test-button"),
                id="submit-test-collapse",
                is_open=False,
                className="mb-4 text-center",
            ),
            ResultsChart,
            # storage
            dcc.Store(
                id="questions-storage",
                data=read_questions("you"),
                storage_type="memory",
            ),
            dcc.Store(id="question-count-storage", data=0),
            dcc.Store(id="answers-storage", data={}, storage_type="memory"),
            dcc.Store(id="lb-visited-last-storage"),
            dcc.Store(id="last-question-visited", data=False),
            dcc.Store(id="personal-answers"),
            dcc.Interval(id="page-load-interval", interval=1, max_intervals=1),
            # download
            dcc.Download(id="download-report"),
        ]
    )


# submit personal questionnaire
@callback(
    [
        Output("personal-questionnaire-collapse", "is_open"),
        Output("question-card-collapse", "is_open"),
        Output("personal-questionnaire-error", "hidden"),
        Output("personal-answers", "data"),
        Output("personal-questionnaire-error", "children"),
    ],
    Input("submit-personal-questionnaire", "n_clicks"),
    [
        State("age", "value"),
        State("relationship-status", "value"),
        State("gender", "value"),
        State("therapy-experience", "value"),
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
            return (
                True,
                False,
                False,
                {},
                "Please fill out all fields before continuing",
            )
    return True, False, True, {}, ""


# shuffle questions on page load
@callback(
    [
        Output("questions-storage", "data"),
        Output("question-text", "children", allow_duplicate=True),
    ],
    Input("page-load-interval", "n_intervals"),
    State("questions-storage", "data"),
    prevent_initial_call=True,
)
def shuffle_questions(n, questions):
    shuffle(questions)
    return questions, questions[0][0]


# show submit button after last question visited
@callback(
    Output("submit-test-collapse", "is_open"),
    Input("last-question-visited", "data"),
)
def show_submit_button(last_question_visited: bool) -> bool:
    return last_question_visited


# switch subject
@callback(
    [
        Output("questions-storage", "data", allow_duplicate=True),
        Output("question-count-storage", "data", allow_duplicate=True),
        Output("answers-storage", "data", allow_duplicate=True),
        Output("question-text", "children", allow_duplicate=True),
        Output("question-count-text", "children", allow_duplicate=True),
        Output("submit-test-collapse", "is_open", allow_duplicate=True),
        Output("dashboard-collapse", "is_open", allow_duplicate=True),
        Output("last-question-visited", "data", allow_duplicate=True),
    ],
    [Input("assess-yourself", "n_clicks"), Input("asses-others", "n_clicks")],
    prevent_initial_call=True,
)
def switch_subject(yourself_clicks, partner_clicks):
    id_triggered = ctx.triggered_id
    if id_triggered == "assess-yourself":
        questions = read_questions("you")
        shuffle(questions)
        return (
            questions,
            1,
            {},
            questions[0][0],
            f"Question 1/{len(questions)}",
            False,
            False,
            False,
        )
    else:
        questions = read_questions("partner")
        shuffle(questions)
        return (
            questions,
            1,
            {},
            questions[0][0],
            f"Question 1/{len(questions)}",
            False,
            False,
            False,
        )


@callback(
    [
        Output("dashboard-collapse", "is_open"),
        Output("pie-chart", "figure"),
        Output("type-description-markdown", "children"),
    ],
    Input("submit-test-button", "n_clicks"),
    [
        State("answers-storage", "data"),
        State("question-count-storage", "data"),
        State("questions-storage", "data"),
        State("slider", "value"),
        State("personal-answers", "data"),
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

        print(answers)
        # fig = build_pie_chart(
        #     anxious_score=anxious_score,
        #     secure_score=secure_score,
        #     avoidant_score=avoidant_score,
        # )
        fig = build_ecr_r_chart(
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


@callback(
    Output("download-report", "data"),
    Input("download-report-button", "n_clicks"),
    State("answers-storage", "data"),
    prevent_initial_call=True,
)
def load_report(n_clicks, answers):
    if n_clicks:
        answers = revert_questions(answers)
        generate_report(answers)
        return dcc.send_file("tmp/attachment_style_report.pdf", type="pdf")


@callback(
    [
        Output("question-count-storage", "data"),
        Output("question-count-text", "children"),
        Output("question-text", "children"),
        Output("answers-storage", "data"),
        Output("slider", "value"),
        Output("lb-visited-last-storage", "data"),
        Output("last-question-visited", "data"),
    ],
    [
        Input("right-button", "n_clicks"),
        Input("left-button", "n_clicks"),
    ],
    [
        State("slider", "value"),
        State("question-count-storage", "data"),
        State("questions-storage", "data"),
        State("answers-storage", "data"),
        State("lb-visited-last-storage", "data"),
        State("last-question-visited", "data"),
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
            case "right-button":
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

            case "left-button":
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
            case "right-button":
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

            case "slider":
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

            case "left-button":
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


clientside_callback(
    """
    function(trigger) {
        if (!window.arrowKeysListenerAttached) {
            function ArrowClick(event) {
                if (event.key === "ArrowRight") {
                    document.getElementById('right-button').click();
                } else if (event.key === "ArrowLeft") {
                    document.getElementById('left-button').click();
                }
            }
            
            window.addEventListener('keydown', ArrowClick);
            window.arrowKeysListenerAttached = true; 
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("dummy-for-keydown", "style"),
    Input("dummy-for-keydown", "style"),
)

