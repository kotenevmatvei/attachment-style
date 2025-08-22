
def layout(**kwargs):
    return html.Div(
        [
            html.Div(id="dummy-div-keys"),
            html.Div(id="dummy-div-pic-download"),
            html.H3("Assess Yourself", className="text-center"),
            dbc.Collapse(
                DemographicsQuestionnaire,
                id="personal-questionnaire-collapse",
                is_open=True,
            ),
            # dbc.Collapse(
            #     [
            #         dcc.Markdown(
            #             """
            #             Please adjust the slider below to evaluate how much you can
            #             relate to the following statements on the scale from 0 to 10.
            #             (e.g. 4 meaning you can agree 40% of the time).
            #             You can use the back and forth buttons to navigate between questions.
            #             """,
            #             className="text-center",
            #         ),
            #         QuestionCard,
            #     ],
            #     id="question-card-collapse",
            #     is_open=False,
            # ),
            # dbc.Collapse(
            #     dbc.Button("To Results", id="submit-test-button"),
            #     id="submit-test-collapse",
            #     is_open=False,
            #     className="mb-4 text-center",
            # ),
            # ResultsChart,
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
            dcc.Store(id="figure-store"),
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


# shuffle questions on page load -- comment out when testing!
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
    [Input("assess-yourself", "n_clicks"), Input("assess-others", "n_clicks")],
    prevent_initial_call=True,
)
def switch_subject(yourself_clicks, others_clicks):
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
        questions = read_questions("others")
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
        Output("figure-store", "data"),
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
        ### testing ###
        # anxious_scores_before_revert = [answers[_][1] for _ in answers.keys() if answers[_][0] == "anxious"]
        # avoidant_scores_before_revert = [answers[_][1] for _ in answers.keys() if answers[_][0] == "avoidant"]
        # scores_before_revert = (
        #     anxious_scores_before_revert + avoidant_scores_before_revert
        # )

        answers = revert_questions(answers)

        ### testing ###
        # anxious_scores_after_revert = [answers[_][1] for _ in answers.keys() if answers[_][0] == "anxious"]
        # avoidant_scores_after_revert = [answers[_][1] for _ in answers.keys() if answers[_][0] == "avoidant"]
        # scores_after_revert = (
        #     anxious_scores_after_revert + avoidant_scores_after_revert
        # )

        (anxious_score, secure_score, avoidant_score) = calculate_scores(answers)

        if anxious_score >= secure_score and anxious_score >= avoidant_score:
            description = generate_type_description("anxious")
        if secure_score >= avoidant_score and secure_score >= anxious_score:
            description = generate_type_description("secure")
        if avoidant_score >= secure_score and avoidant_score >= anxious_score:
            description = generate_type_description("avoidant")

        logger.info("Building the ecr_r chart for browser...")
        fig = build_ecr_r_chart(
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
    Output("dummy-div-pic-download", "style"),
    Input("figure-store", "data"),
    prevent_initial_call=True,
)
def download_plot_picture(fig_json):

    fig = pio.from_json(fig_json)

    logger.info("Saving the image...")
    fig.write_image(
        "tmp/figure_you.png", width=700, height=500
    )
    logger.info("Image saved")

    return {}


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
                answers[f"{question_count - 1}"] = (
                    questions[question_count - 1][1],
                    slider_value,
                    questions[question_count - 1][0],
                )
                # questions between first and one before last one
                if question_count < n - 1:
                    question_count += 1
                    if f"{question_count - 1}" in answers.keys():
                        return (
                            question_count,
                            f"Question {question_count}/{n}",
                            questions[question_count - 1][0],
                            answers,
                            answers[f"{question_count - 1}"][1],
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
                    if f"{question_count - 1}" in answers.keys():
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
                    if f"{question_count - 1}" in answers.keys():
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
                        if f"{question_count - 1}" in answers.keys():
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
    return (1, f"Question {1}/{n}", questions[0][0], answers, 1, False, False)


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
    Output("dummy-div-keys", "style"),
    Input("dummy-div-keys", "style"),
)
