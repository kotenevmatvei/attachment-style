from dash import Dash, html, dcc, Input, Output, State, ctx
from random import shuffle
from sqlalchemy.orm import Session
import copy
import plotly.io as pio
import dash_bootstrap_components as dbc

from components.navbar import Navbar
from components.description import Description
from components.question_card import QuestionCard
from components.dashboard import Dashboard

from utils.utils import read_questions, calculate_scores, build_pie_chart, generate_type_description, increase_figure_font, upload_to_db
from utils.generate_pdf import generate_report

from models import TestYourself

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP])
server = app.server

app.layout = dbc.Container(
    [
        Navbar,
        Description,
        QuestionCard,
        dbc.Collapse(dbc.Button("Submit Test", id="submit-test-button"), id="submit-test-collapse", is_open=False, className="mb-4 text-center"),
        Dashboard,
        dbc.Collapse(dbc.Button("Download Full Report", id="download-report-button"), id="download-report-collapse", is_open=False, className="mb-4 text-center"),
        dbc.Collapse(dcc.Markdown("Thank you for trying out the attachment style test!", className="mt-4 text-center"), id="thank-you-collapse", is_open=False),
        # storage
        dcc.Store(id="questions-storage", data=read_questions("you"), storage_type="memory"),
        dcc.Store(id="question-count-storage", data=0),
        dcc.Store(id="answers-storage", data={}, storage_type="memory"),
        dcc.Store(id="lb-visited-last-storage"),
        dcc.Store(id="last-question-visited"),
        dcc.Store(id="current-subject-storage", data="you"),
        dcc.Interval(id="page-load-interval", interval=1, max_intervals=1),
        # download
        dcc.Download(id="download-report")
    ],
)

# shuffle questions on page load
@app.callback(
    [
        Output('questions-storage', 'data'),
        Output("question-text", "children", allow_duplicate=True)
    ],
    Input('page-load-interval', 'n_intervals'),
    State("questions-storage", "data"),
    prevent_initial_call=True
)
def shuffle_questions(n, questions):
    shuffle(questions)
    return questions, questions[0][0]


# show submit button after last question visited
@app.callback(
    Output("submit-test-collapse", "is_open"),
    Input("last-question-visited", "data"),
)
def show_submit_button(last_question_visited: bool) -> bool:
    return last_question_visited


# switch subject
@app.callback(
    [
        Output("questions-storage", "data", allow_duplicate=True),
        Output("question-count-storage", "data", allow_duplicate=True),
        Output("answers-storage", "data", allow_duplicate=True),
        Output("question-text", "children", allow_duplicate=True),
        Output("question-count-text", "children", allow_duplicate=True),
        Output("submit-test-collapse", "is_open", allow_duplicate=True),
        Output("dashboard-collapse", "is_open", allow_duplicate=True),
        Output("download-report-collapse", "is_open", allow_duplicate=True),
        Output("thank-you-collapse", "is_open", allow_duplicate=True),
        Output("last-question-visited", "data", allow_duplicate=True)

    ],
    [
        Input("test-yourself", "n_clicks"),
        Input("test-your-partner", "n_clicks")
    ],
    prevent_initial_call=True
)
def switch_subject(yourself_clicks, partner_clicks):
    id_triggered = ctx.triggered_id
    if id_triggered == "test-yourself":
        questions = read_questions("you")
        shuffle(questions)
        return questions, 1, {}, questions[0][0], f"Question 1/{len(questions)}", False, False, False, False, False
    else:
        questions = read_questions("partner")
        shuffle(questions)
        return questions, 1, {}, questions[0][0], f"Question 1/{len(questions)}", False, False, False, False, False


@app.callback(
    [
        Output("dashboard-collapse", "is_open"),
        Output("pie-chart", "figure"),
        Output("type-description-markdown", "children"),
        Output("download-report-collapse", "is_open")
    ],
    Input("submit-test-button", "n_clicks"),
    [
        State("answers-storage", "data"),
        State("question-count-storage", "data"),
        State("questions-storage", "data"),
        State("slider", "value")
    ],
    prevent_initial_call=True,
)
def generate_dashboard(n_clicks, answers, question_count, questions, slider_value):
    if question_count == len(questions):
        answers[f"{question_count-1}"] = (questions[question_count-1][1], slider_value, questions[question_count-1][0])
    # load to db
    upload_to_db(answers)
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

        pio.write_image(fig_to_download, 'data/figure.png', width=700 * 1.5, height=500 * 1.5)
        return True, fig, description, True


@app.callback(
    [
        Output("thank-you-collapse", "is_open"),
        Output("download-report", "data")
    ],
    Input("download-report-button", "n_clicks"),
    State("answers-storage", "data"),
    prevent_initial_call=True,
)
def load_report(n_clicks, answers):
    if n_clicks:
        generate_report(answers)
        return True, dcc.send_file("data/attachment style report.pdf", type="pdf")


@app.callback(
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
        Input("slider", "value")
    ],
    [
        State("question-count-storage", "data"),
        State("questions-storage", "data"),
        State("answers-storage", "data"),
        State("lb-visited-last-storage", "data"),
        State("last-question-visited", "data"),
    ]
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
                answers[f"{question_count-1}"] = (questions[question_count-1][1], slider_value, questions[question_count-1][0])
                # questions between first and one before last one
                if question_count < n-1:
                    question_count += 1
                    if f"{question_count-1}" in answers.keys():
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count-1][0],
                            answers,
                            answers[f"{question_count-1}"][1],
                            False,
                            False
                        )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count-1][0],
                            answers,
                            0,
                            False,
                            False
                        )
                # question before last one (show submit button next)
                elif question_count == n-1:
                    question_count += 1
                    if f"{question_count-1}" in answers.keys():
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count-1][0],
                            answers,
                            answers[f"{question_count-1}"][1],
                            False,
                            True
                        )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count-1][0],
                            answers,
                            0,
                            False,
                            True
                        )
                # last question
                else:
                    return (
                        question_count,
                        f"Question {n}/{n}",
                        questions[n-1][0],
                        answers,
                        answers[f"{question_count-1}"][1],
                        False,
                        True
                    )

            case "slider":
                answers[f"{question_count - 1}"] = (questions[question_count - 1][1], slider_value, questions[question_count-1][0])
                # questions between first and last
                if question_count < n-1:
                    if not lb_visited_last:
                        question_count += 1
                        if f"{question_count-1}" in answers.keys():
                            return (
                                question_count,
                                f"Question {question_count}/{n}",
                                questions[question_count - 1][0],
                                answers,
                                answers[f"{question_count-1}"][1],
                                False,
                                False
                            )
                        else:
                            return (
                                question_count,
                                f"Question {question_count}/{n}",
                                questions[question_count - 1][0],
                                answers,
                                0,
                                False,
                                False
                            )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            answers[f"{question_count-1}"][1],
                            False,
                            False
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
                            answers[f"{question_count - 1}"][1],
                            False,
                            True
                        )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            0,
                            False,
                            True
                        )
                # last question
                else:
                    return (
                        question_count,
                        f"Question {n}/{n}",
                        questions[n - 1][0],
                        answers,
                        answers[f"{question_count - 1}"][1],
                        False,
                        True
                    )

            case "left-button":
                if question_count == 1:
                    answers["0"] = (questions[0][1], slider_value, questions[question_count-1][0])
                    return (
                        1,
                        f"Question 1/{n}",
                        questions[0][0],
                        answers,
                        answers["0"][1],
                        True,
                        False
                    )
                else:
                    answers[f"{question_count-1}"] = (questions[question_count-1][1], slider_value, questions[question_count-1][0])
                    return (
                        question_count-1,
                        f"Question {question_count-1}/{n}",
                        questions[question_count-2][0],
                        answers,
                        answers[f"{question_count - 2}"][1],
                        True,
                        False
                    )

    else:
        match id_triggered:
            case "right-button":
                # questions between first and last
                if question_count < n:
                    answers[f"{question_count - 1}"] = (questions[question_count - 1][1], slider_value, questions[question_count-1][0])
                    question_count += 1
                    if f"{question_count-1}" in answers.keys():
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            answers[f"{question_count - 1}"][1],
                            False,
                            True
                        )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            0,
                            False,
                            True
                        )
                # last question
                else:
                    answers[f"{question_count - 1}"] = (questions[question_count - 1][1], slider_value, questions[question_count-1][0])
                    return (
                        question_count,
                        f"Question {n}/{n}",
                        questions[n - 1][0],
                        answers,
                        answers[f"{question_count - 1}"][1],
                        False,
                        True
                    )

            case "slider":
                # questions between first and last
                if question_count < n:
                    answers[f"{question_count - 1}"] = (questions[question_count - 1][1], slider_value, questions[question_count-1][0])
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
                                True
                            )
                        else:
                            return (
                                question_count,
                                f"Question {question_count}/{n}",
                                questions[question_count - 1][0],
                                answers,
                                0,
                                False,
                                True
                            )
                    else:
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            answers[f"{question_count - 1}"][1],
                            False,
                            True
                        )
                # last question
                else:
                    answers[f"{question_count - 1}"] = (questions[question_count - 1][1], slider_value, questions[question_count-1][0])
                    return (
                        question_count,
                        f"Question {n}/{n}",
                        questions[n - 1][0],
                        answers,
                        answers[f"{question_count - 1}"][1],
                        False,
                        True
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
                        True
                    )
                else:
                    answers[f"{question_count - 1}"] = (questions[question_count - 1][1], slider_value, questions[question_count-1][0])
                    return (
                        question_count - 1,
                        f"Question {question_count - 1}/{n}",
                        questions[question_count - 2][0],
                        answers,
                        answers[f"{question_count - 2}"][1],
                        True,
                        True
                    )

    # first question / initial state
    return (
        1,
        f"Question {1}/{n}",
        questions[0][0],
        answers,
        0,
        False,
        False
    )

if __name__ == "__main__":
    app.run_server(debug=True)
