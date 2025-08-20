import dash_mantine_components as dmc
import constants

SubjectSwitch = dmc.Container(
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
                    "Test yourself",
                    variant="gradient",
                    size="lg",
                    m="lg",
                    radius="xl",
                ),
                dmc.Button(
                    "Test others",
                    variant="gradient",
                    m="lg",
                    size="lg",
                    radius="xl",
                ),
            ],
        ),
    ]
)
