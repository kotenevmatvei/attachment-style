import dash_mantine_components as dmc
from dash import dcc
from dash_iconify import DashIconify

import constants
from data.options import attachment_style_labels_values, demographics_radio_options

dmc.add_figure_templates()

BoxCard = dmc.Card(
    children=[
        dmc.CardSection(
            dmc.SimpleGrid(
                cols=3,
                children=[
                    dmc.Space(w="xs"),
                    dmc.Title("Box Plot", order=2, ta="center", c=constants.PRIMARY),
                    dmc.Flex(
                        dmc.Button(
                            DashIconify(icon="material-symbols:help-outline", width=25, color=constants.PRIMARY),
                            id="box-info-modal-button",
                            variant="light",
                            radius="md"
                        ),
                        justify="right",
                        align="center",
                    )
                ]
            ),
            withBorder=True, p="md", mb="xs",
        ),
        # dmc.CardSection("Box Plot", withBorder=True, p="md", c=constants.PRIMARY),
        dmc.RadioGroup(
            label="Select demographic variable",
            id="demographic-radio",
            children=dmc.Group([dmc.Radio(l, value=k) for k, l in demographics_radio_options]),
            size="md",
            value="gender",
            mb="xs",
        ),
        dmc.Select(
            label="Select attachment style",
            id="attachment-style-dropdown-demographics",
            data=attachment_style_labels_values,
            value="avoidant_score",
            size="md",
            mb="xs",
        ),
        dcc.Graph(id="box-graph"),

        dmc.Modal(
            title=dmc.Title("Box Plot", order=3),
            id="box-info-modal",
            shadow="xl",
            padding=25,
            size="lg",
            children=[
                dmc.Image(src="assets/boxplot_info.jpg"),
                dmc.Text(
                    "A box plot is a standardized way to display data distribution using five key statistical measures "
                    "that reveal the spread and central tendency of a dataset. This visualization method provides a quick "
                    "overview of data symmetry, variability, and potential outliers without showing every individual data point."
                ),
                dmc.Space(h="md"),
                dmc.Text("Key Components", fw="bold"),
                dmc.Space(h="md"),
                dmc.Text(
                    "The box plot consists of several distinct elements that each represent specific statistical "
                    "measures. The box itself spans from the first quartile (Q1) to the third quartile (Q3), "
                    "containing the middle 50% of the data. A line inside the box marks the median (Q2), which "
                    "divides the dataset into two equal halves."
                ),
                dmc.Space(h="md"),
                dmc.Text(
                        "The whiskers extend from the box to show the range of data within 1.5 times the interquartile range "
                        "(IQR) from the box edges. Any data points beyond the whiskers appear as individual dots and "
                        "represent outliers - values that are unusually high or low compared to the rest of the dataset."
                ),
                dmc.Space(h="md"),
                dmc.Text("Reading the Plot", fw="bold"),
                dmc.Space(h="md"),
                dmc.Text(
                    "Box plots make it easy to identify several data characteristics at a glance. A longer box indicates "
                    "greater variability in the middle 50% of data, while the position of the median line within the box "
                    "reveals skewness. If the median line sits closer to Q1, the data is right-skewed; if closer to Q3, "
                    "it's left-skewed."
                ),
                dmc.Space(h="md"),
                dmc.Space(h="md"),
                dmc.Text(
                    "The length of the whiskers shows the spread of the outer data ranges, and the presence of outlier "
                    "points immediately highlights unusual values that might warrant further investigation. This makes "
                    "box plots particularly valuable for comparing multiple datasets side by side, as differences in "
                    "central tendency, spread, and skewness become immediately apparent."
                ),
            ]
        )
    ],
    withBorder=True,
    shadow="md",
    radius="md",
    w=600,
)
