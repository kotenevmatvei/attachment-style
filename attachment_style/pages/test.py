from dash import register_page, Output, Input, State, callback
import dash_mantine_components as dmc

from components.demographics_questionnaire import DemographicsQuestionnaireRevised
# from components.question_card import QuestionCard
from components.question_card import QuestionComponent
from components.results import ResultsBoard
from components.subject_switch import SubjectSwitch

register_page(__name__, path="/")


def layout(**kwargs):
    return dmc.Container(
        mt="lg",
        children=[
            dmc.Collapse(
                id="subject-switch-collapse",
                opened=True,
                children=[
                    SubjectSwitch,
                ]
            ),
            dmc.Collapse(
                id="demographics-questionnaire-collapse",
                opened=False,
                children=[
                    DemographicsQuestionnaireRevised,
                ]
            ),
            dmc.Collapse(
                opened=False,
                id="question-card-collapse",
                children=[
                    QuestionComponent,
                ]
            ),
            dmc.Collapse(
                opened=False,
                id="results-board-collapse",
                children=[
                    ResultsBoard
                ]
            ),
        ]
    )

