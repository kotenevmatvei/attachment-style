from dash import callback, Output, Input, State

# update the score cards on top
@callback(
    [
        Output("anxious-score-percent-text", "children"),
        Output("avoidant-score-percent-text", "children"),
        Output("secure-score-percent-text", "children"),
    ],
    Input("result-scores-store", "data"),
    prevent_initial_callback=True,
)
def update_score_cards(scores):
    # convert to relative percentage
    total_score = scores["anxious_score"] + scores["avoidant_score"] + scores["secure_score"]
    anxious_percent = round(((scores["anxious_score"] / total_score) * 100), 1)
    avoidant_percent = round(((scores["avoidant_score"] / total_score) * 100), 1)
    secure_percent = round(((scores["secure_score"] / total_score) * 100), 1)
    return (
        f"{anxious_percent}%",
        f"{avoidant_percent}%",
        f"{secure_percent}%",
    )
