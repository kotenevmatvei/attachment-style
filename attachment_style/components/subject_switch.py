from dash import callback, Input, Output
import dash_mantine_components as dmc
import constants

SubjectSwitch = dmc.Paper(
    withBorder=True,
    radius="xl",
    shadow="lg",
    mt="xl",
    p="xl",
    pt="xl",
    children=[
        dmc.Center(
            dmc.Title(
                "Would you like to test yourself or someone else?",
                c=constants.PRIMARY,
                mb="lg",
            ),
        ),
        dmc.Flex(
            align="center",
            justify="center",
            children=[
                dmc.Button(
                    "Assess yourself",
                    id="assess-yourself-button",
                    variant="gradient",
                    gradient={"from": constants.PRIMARY, "to": "cyan"},
                    size="lg",
                    m="lg",
                    radius="xl",
                ),
                dmc.Button(
                    "Assess others",
                    id="assess-others-button",
                    variant="gradient",
                    gradient={"from": constants.PRIMARY, "to": "cyan"},
                    m="lg",
                    size="lg",
                    radius="xl",
                ),
            ],
        ),
    ]
)


@callback(
    [
        Output("demographics-questionnaire-collapse", "opened", allow_duplicate=True),
        Output("subject-switch-collapse", "opened")
    ],
    [
        Input("assess-yourself-button", "n_clicks"),
        Input("assess-others-button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def toggle_demographics_questionnaire(assess_yourself_click, assess_others_click):
    if assess_yourself_click:
        return True, False
    elif assess_others_click:
        return True, False
    return False, True

