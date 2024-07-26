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
            html.H1("3D Chart"),
            dcc.Graph(figure=fig),
        ]
    )