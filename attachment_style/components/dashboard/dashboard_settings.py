import dash_mantine_components as dmc
from dash_iconify import DashIconify

DashboardSettings = dmc.Flex(
    gap="md",
    justify="center",
    align="center",
    direction="row",
    wrap="wrap",
    mb="md",
    children=[
        dmc.Button(
            "Refresh Data",
            leftSection=DashIconify(
                icon="tabler:refresh", width=16
            ),
            variant="light",
            id="refresh-data-button",
        ),
        dmc.Text("Select the dataset:", size="lg"),
        dmc.MultiSelect(
            # label="Select the dataset:",
            data=[
                {"label": "Assess Yourself", "value": "assess_yourself"},
                {"label": "Assess Others", "value": "assess_others"},
            ],
            value=["assess_yourself", "assess_others"],
            size="lg",
            comboboxProps={"shadow": "lg"},
        ),
        dmc.Switch("Include test data", size="lg", mr="xs", id="include-test-data-button"),
    ],
)
