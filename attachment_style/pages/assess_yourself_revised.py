from dash import register_page
import dash_mantine_components as dmc
import logging

from components.demographics_questionnaire_revised import DemographicsQuestionnaire

register_page(__name__, path="/assess-yourself-revised")

def layout(**kwargs):
    return dmc.Container(
        mt="lg",
        children=[
            # dmc.Title("Assess Yourself"),
            DemographicsQuestionnaire
        ]
    )
