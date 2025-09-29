from dash import callback, Input, Output, State


# don't leave error messages there until the user tries to submit again
@callback(
    Output("age-select", "error", allow_duplicate=True),
    Input("age-select", "value"),
    prevent_initial_call=True,
)
def validate_age(age_value):
    return None

@callback(
    Output("relationship-status-select", "error", allow_duplicate=True),
    Input("relationship-status-select", "value"),
    prevent_initial_call=True,
)
def validate_age(age_value):
    return None

@callback(
    Output("therapy-experience-select", "error", allow_duplicate=True),
    Input("therapy-experience-select", "value"),
    prevent_initial_call=True,
)
def validate_age(age_value):
    return None

@callback(
    Output("gender-select", "error", allow_duplicate=True),
    Input("gender-select", "value"),
    prevent_initial_call=True,
)
def validate_age(age_value):
    return None


# submit personal questionnaire
@callback(
    [
        Output("demographics-questionnaire-collapse", "opened"),
        Output("question-card-collapse", "opened"),

        Output("age-select", "error"),
        Output("relationship-status-select", "error"),
        Output("therapy-experience-select", "error"),
        Output("gender-select", "error"),

        Output("demographics-answers-store", "data"),
    ],
    Input("continue-to-test-button", "n_clicks"),
    [
        State("age-select", "value"),
        State("relationship-status-select", "value"),
        State("gender-select", "value"),
        State("therapy-experience-select", "value"),
    ],
    prevent_initial_call=True,
)
def submit_personal_questionnaire(
        n_clicks, age, relationship_status, gender, therapy_experience
):
    if n_clicks:
        if all([age, relationship_status, gender, therapy_experience]):
            print("i am on the wrong path")
            demographics_answers = {
                "age": age,
                "relationship_status": relationship_status,
                "gender": gender,
                "therapy_experience": therapy_experience,
            }
            print(demographics_answers)
            return (
                False, True,
                None, None, None, None,
                demographics_answers
            )

        age_error = "Please select your age" if not age else None
        relationship_status_error = "Please select your relationship status" if not relationship_status else None
        therapy_experience_error = "Please select your therapy experience" if not therapy_experience else None
        gender_error = "Please select your gender" if not gender else None
        print("i am on the right path")
        return (
            True, False,
            age_error, relationship_status_error, therapy_experience_error, gender_error,
            {}
        )

    print("i am on the second wrong path")
    return False, False, None, None, None, None, {}
