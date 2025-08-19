from dash import register_page, Output, Input, State, callback
import dash_mantine_components as dmc

from components.demographics_questionnaire_revised import DemographicsQuestionnaire
from components.question_card import QuestionCard
from components.question_card_revised import QuestionComponent
from components.results_revised import build_results_board
from components.subject_switch import SubjectSwitch

register_page(__name__, path="/assess-yourself-revised")

def layout(**kwargs):
    return dmc.Container(
        mt="lg",
        children=[
            SubjectSwitch,
            DemographicsQuestionnaire,
            QuestionComponent,
            build_results_board(),
        ]
    )

# submit personal questionnaire
# @callback(
#     [
#         Output("personal-questionnaire-collapse", "is_open"),
#         Output("question-card-collapse", "is_open"),
#         Output("personal-questionnaire-error", "hidden"),
#         Output("personal-answers", "data"),
#         Output("personal-questionnaire-error", "children"),
#     ],
#     Input("submit-personal-questionnaire", "n_clicks"),
#     [
#         State("age-input", "value"),
#         State("relationship-status-input", "value"),
#         State("gender-input", "value"),
#         State("therapy-experience-input", "value"),
#     ],
# )
# def sumbmit_personal_questionnaire(
#     n_clicks, age, relationship_status, gender, therapy_experience
# ):
#     if n_clicks:
#         if all([age, relationship_status, gender, therapy_experience]):
#             if age < 0 or age > 100:
#                 return True, False, False, {}, "Please enter a valid age"
#             return (
#                 False,
#                 True,
#                 True,
#                 {
#                     "age": age,
#                     "relationship_status": relationship_status,
#                     "gender": gender,
#                     "therapy_experience": therapy_experience,
#                 },
#                 "",
#             )
# 
#         else:
#             return (
#                 True,
#                 False,
#                 False,
#                 {},
#                 "Please fill out all fields before continuing",
#             )
#     return True, False, True, {}, ""
