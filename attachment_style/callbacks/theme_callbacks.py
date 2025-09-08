from dash import Output, Input, callback, State
import dash_mantine_components as dmc


# toggle theme by clicking the button in the header
@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(_, theme):
    return "dark" if theme == "light" else "light"


# question card - answer options
@callback(
    [Output("question-paper", "style")]
    + [Output(f"option-{i}", "bg") for i in range(1, 8)]
    + [Output(f"option-{i}", "c") for i in range(1, 8)],
    Input("mantine-provider", "forceColorScheme"),
    )
def update_question_card_style(theme):
    if theme == "dark":
        return (
            {"backgroundColor": dmc.DEFAULT_THEME["colors"]["dark"][6]},
            *["dark" for i in range(1, 8)],
            *["white" for i in range(1, 8)]
            # *[dmc.DEFAULT_THEME["colors"]["dark"][7] for i in range(1,8)]
        )
    else:
        return (
            {"backgroundColor": dmc.DEFAULT_THEME["colors"]["gray"][1]},
            *["gray.1" for i in range(1, 8)],
            *["black" for i in range(1, 8)]
            # *[dmc.DEFAULT_THEME["colors"]["dark"][1] for i in range(1,8)]
        )

# report download paper
@callback(
    Output("download-paper", "style"),
    Input("mantine-provider", "forceColorScheme"),
)
def update_download_paper_style(color_scheme):
    if color_scheme == "dark":
        return {
            "background": f"linear-gradient(135deg, {dmc.DEFAULT_THEME['colors']['dark'][8]} 0%, "
                          f"{dmc.DEFAULT_THEME['colors']['dark'][6]} 100%)"
        }
    return {"background": "linear-gradient(135deg, #FFF5F5 0%, #FFF8DC 100%)"}


