import dash_mantine_components as dmc
from dash_iconify import DashIconify

Stepper = dmc.Stepper(
    id="test-stepper",
    active=0,
    mb="lg",
    display={"base": "None", "sm": "block"},
    children=[
        dmc.StepperStep(
            label="Subject",
            description="Who is the subject?",
            allowStepSelect=False,
        ),
        dmc.StepperStep(
            label="Demographics",
            description="Tell us about you",
            allowStepSelect=False,
        ),
        dmc.StepperStep(
            label="Questionnaire",
            description="Answer the questions",
            allowStepSelect=False,
        ),
        dmc.StepperStep(
            label="Results",
            description="Download your report!",
            allowStepSelect=False,
        ),
    ]
)

StepperMobile = dmc.Stepper(
    id="test-stepper-mobile",
    mt=0,
    mb=0,
    active=0,
    display={"base": "block", "sm": "None"},
    children=[
        dmc.StepperStep(
            icon=DashIconify(icon="tabler:users", height=20),
            allowStepSelect=False,
        ),
        dmc.StepperStep(
            icon=DashIconify(icon="tabler:clipboard-list", height=20),
            allowStepSelect=False,
        ),
        dmc.StepperStep(
            icon=DashIconify(icon="tabler:file-analytics", height=20),
            allowStepSelect=False,
        ),
        dmc.StepperStep(
            icon=DashIconify(icon="tabler:report-analytics", height=20),
            allowStepSelect=False,
        ),
    ]
)
