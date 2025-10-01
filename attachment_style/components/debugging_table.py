"""
I want a table summarizing the current state.
Columns:
    * question_ind
    * score
    * question_text
Styling:
    * red background for the current_question
    * gray background for all answered questions
    * white for all unanswered
"""
import dash_mantine_components as dmc
from dash import callback, Input, Output, ALL
import logging

from sqlalchemy.sql.functions import current_date

logger = logging.getLogger(__name__)

DebuggingTable = dmc.Container(
    id="debugging-container",
)

CurrentCount = dmc.Container(
    children=[
        dmc.Badge(id="debug-current-question"),
        dmc.Badge(id="debug-answered-questions"),
    ]
)


@callback(
[
    Output("debugging-container", "children"),
    Output("debug-current-question", "children"),
    Output("debug-answered-questions", "children"),
],
[
    Input("answers-store", "data"),
    Input("current-question-count-store", "data"),
    Input("questions-answered-count-store", "data"),
]
)
def update_answers_in_debug_table(answers, current_question, questions_answered):
    # logger.info("Drawing the table")
    head = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("Index"),
                dmc.TableTh("Text"),
                dmc.TableTh("Score"),
            ]
        )
    )
    rows = []
    for i, (key, value) in enumerate(answers.items(), start=1):
        if value:
            if i == current_question:
                style = {"backgroundColor": "red"}
            elif i <= questions_answered:
                style = {"backgroundColor": "gray"}
            else:
                style = {"backgroundColor": "white"}
            rows.append(
                dmc.TableTr(
                    children=[
                        dmc.TableTd(key),
                        dmc.TableTd(value["question_text"]),
                        dmc.TableTd(value["score"]),
                    ],
                    style=style,
                )
            )
        else:
            if i == current_question:
                style = {"backgroundColor": "red"}
            elif i <= questions_answered:
                style = {"backgroundColor": "gray"}
            else:
                style = {"backgroundColor": "white"}
            rows.append(
                dmc.TableTr(
                    children=[
                        dmc.TableTd(key),
                        dmc.TableTd("None"),
                        dmc.TableTd("None"),
                    ],
                    style=style
                )
            )

    body = dmc.TableTbody(rows)
    caption = dmc.TableCaption("Debugging table")
    table = dmc.Table([head, body, caption])
    # logger.info(f"just drew the table with {len(rows)} rows")

    return table, current_question, questions_answered

