import os
from sqlalchemy import create_engine
from dash import Dash, html, dcc, Input, Output, State, ctx, page_container, callback, register_page
from sqlalchemy.orm import Session
from utils.utils import get_data_from_db, aggregate_scores, create_3d_chart

register_page(__name__)

# get the data from the database
ty, tp = get_data_from_db()
aggregate_scores(ty, tp)
# create a plot
fig = create_3d_chart(ty, tp, "you", "gender")

def layout(**kwargs):
    return html.Div(
        [
            html.H1("3D Chart", className="text-center"),
            # add dropdowns to choose gender, relationship_status, therapy_experience
            html.Div(
                [
                    html.Label("Gender"),
                    dcc.Dropdown(
                        id="gender-dropdown",
                        options=[
                            {"label": "Male", "value": "male"},
                            {"label": "Female", "value": "female"},
                            {"label": "Other", "value": "other"},
                        ],
                        value="male",
                    ),
                    html.Label("Relationship Status"),
                    dcc.Dropdown(
                        id="relationship-status-dropdown",
                        options=[
                            {"label": "Single", "value": "single"},
                            {"label": "In a Relationship", "value": "relationship"},
                            {"label": "Married", "value": "married"},
                        ],
                        value="single",
                    ),
                    html.Label("Therapy Experience"),
                    dcc.Dropdown(
                        id="therapy-experience-dropdown",
                        options=[
                            {"label": "None", "value": "none"},
                            {"label": "Some", "value": "some"},
                            {"label": "Extensive", "value": "extensive"},
                        ],
                        value="none",
                    ),
                ]
            ),
            dcc.Graph(figure=fig),
        ]
    )