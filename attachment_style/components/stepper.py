import dash_mantine_components as dmc

Stepper = dmc.Stepper(
    id="test-stepper",
    active=0,
    mb="lg",
    children=[
        dmc.StepperStep(
            label="Subject",
            description="Who is the subject?",
        ),
        dmc.StepperStep(
            label="Demographics",
            description="Tell us about you",
        ),
        dmc.StepperStep(
            label="Questionnaire",
            description="Answer the questions",
        ),
        dmc.StepperStep(
            label="Results",
            description="Download your report!",
        ),
    ]
)

