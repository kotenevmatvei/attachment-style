import dash_mantine_components as dmc
from dash import register_page

import constants

register_page(__name__)


def layout(**kwargs):
    return dmc.Container(
        [
            dmc.Center(dmc.Title("About", c=constants.PRIMARY)),
            dmc.Accordion(
                # multiple=True,
                children=[
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl(dmc.Title("Adult Attachment Style Theory", order=4, fw="normal")),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Text(
                                        "Adult attachment styles theory extends John Bowlby's original attachment framework "
                                        "to understand how early caregiver relationships influence adult romantic bonds. "
                                        "The theory has evolved from categorical approaches to a dimensional model focusing "
                                        "on two primary dimensions: attachment anxiety and attachment avoidance."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text("Core Dimensions", fw="bold", c=constants.PRIMARY),
                                    dmc.Text(
                                        "Attachment anxiety reflects the extent to which individuals worry about abandonment "
                                        "and need constant reassurance from partners. Attachment avoidance represents discomfort "
                                        "with intimacy and preference for emotional independence. These dimensions combine to "
                                        "create different attachment patterns in adult relationships."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text("Key Studies and Measures", fw="bold", c=constants.PRIMARY),
                                    dmc.Text(
                                        [
                                            "The most significant advancement came with ",
                                            dmc.Anchor("Brennan, Clark, and Shaver's (1998) ",
                                                       href="https://www.researchgate.net/publication/301325948_Self-report_measurement_of_adult_attachment_An_integrative_overview",
                                                       target="_blank",),
                                            "development of the Experiences in Close Relationships (ECR) scale, followed by ",
                                            dmc.Anchor("Fraley, Waller, and Brennan's (2000) ECR-Revised (ECR-R)", href="https://www.web-research-design.net/PDF/FW&B2000.pdf"),
                                            ". The ECR-R is a 36-item self-report "
                                            "measure that assesses both anxiety and avoidance dimensions, demonstrating excellent "
                                            "reliability with ",
                                            dmc.Anchor("alpha coefficients", href="https://en.wikipedia.org/wiki/Cronbach%27s_alpha"), " near or above 0.90."
                                        ],
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        "The ECR-R has become the most widely used and robust measure of adult attachment, "
                                        "translated into 17 languages and used in hundreds of academic studies. Research "
                                        "using this measure has demonstrated how attachment styles predict relationship "
                                        "satisfaction, emotional regulation, and interpersonal functioning. Studies by "
                                        "Mikulincer and Shaver (2007) found that anxious individuals experience emotional "
                                        "instability, while avoidant individuals withdraw from intimacy, both leading to "
                                        "relationship difficulties."
                                    )
                                ]
                            )
                        ],
                        value="adult-attachment-style-theory",
                    ),
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl(dmc.Title("A More Practical Approach", order=4, fw="normal")),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Text(
                                        "Amir Levine and Rachel Heller made two key modifications to the ECR-R questionnaire "
                                        "in their popular book \"Attached\" to make attachment assessment more practical "
                                        "for everyday relationships."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text("Assessing Others", fw="bold", c=constants.PRIMARY),
                                    dmc.Text(
                                        "The authors created a partner assessment questionnaire titled \"Determining Your "
                                        "Partner's Attachment Style\" that allows individuals to evaluate their romantic "
                                        "partner's attachment behaviors rather than just their own. This modification "
                                        "transforms the self-report nature of the original ECR-R into an observational "
                                        "tool, enabling people to identify attachment patterns in their partners through "
                                        "behavioral indicators and relationship dynamics."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text("Explicit Secure Scoring", fw="bold", c=constants.PRIMARY),
                                    dmc.Text(
                                        "Unlike the traditional ECR-R which primarily measures anxiety and avoidance "
                                        "dimensions, Levine and Heller's version explicitly includes secure attachment "
                                        "as a distinct scored category. Their model uses a four-quadrant system where "
                                        "secure attachment is defined as low avoidance combined with low anxiety, "
                                        "creating a clear secure classification rather than leaving it as simply the "
                                        "absence of insecure traits."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        "The authors designed their modified version to \"work best in everyday life\" "
                                        "by making attachment styles more accessible and actionable for relationship "
                                        "decisions. This approach allows couples to understand both their own and their "
                                        "partner's attachment needs, facilitating better relationship dynamics and "
                                        "communication strategies."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        "Their modifications transformed academic attachment measurement into a practical "
                                        "relationship tool that has reached over two million readers seeking to improve "
                                        "their romantic connections."
                                    )
                                ]
                            )
                        ],
                        value="more-practival-approach",
                    ),
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl(dmc.Title("This Website's Objective", order=4, fw="normal")),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Text(
                                        [
                                            "This website combines two established assessment approaches. The \"Assess Yourself\" "
                                            "questionnaire uses the unmodified ECR-R study format, while the \"Assess Others\" q"
                                            "uestionnaire is based on the version developed by Dr. Amir Levine and Rachel Heller, "
                                            "which I've modified to respect copyright requirements."
                                        ],
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text("Scoring", fw="bold", c=constants.PRIMARY),
                                    dmc.Text(
                                        [
                                            "The \"Assess Others\" questionnaire contains three distinct question groups "
                                            "that test for secure, anxious, and avoidant attachment traits. Each dimension's "
                                            "score is calculated as the average of its corresponding questions.",
                                            dmc.Space(h="md"),
                                            "The \"Assess Yourself\" questionnaire follows the ",
                                            dmc.Anchor("scoring guidelines",
                                                       href="https://centerforhealingkc.com/sites/centerfh/files/ecr-r.pdf"),
                                            " provided in the ECR-R study. This methodology includes reverse-scoring certain "
                                            "questions that ask similar concepts with opposite wording, which helps minimize "
                                            "response bias tendencies.",
                                        ]
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        [
                                            " Since the ECR-R questionnaire doesn't provide an explicit secure attachment score, "
                                            "I mathematically derive one from the anxious and avoidant results. The scoring "
                                            "is normalized so that low anxious and avoidant scores (both at 1) yield a maximum "
                                            "secure score of 7, while high anxious and avoidant scores (both at 7) produce a "
                                            "minimum secure score of 1.",
                                            dmc.Space(h="md"),
                                            dmc.Text(
                                                [
                                                    "This approach serves two purposes. First, it creates consistency across the application—the ",
                                                    dmc.Anchor("dashboard", href="/dashboard"),
                                                    " displays statistics for all three attachment dimensions, allowing "
                                                    "universal use of the same visualization tools for both questionnaires. Second, "
                                                    "this derived score supplements rather than alters the original ECR-R results, "
                                                    "providing an additional metric that helps users better understand their attachment "
                                                    "style profile."
                                                ],
                                            )
                                        ],
                                    ),
                                ]
                            )
                        ],
                        value="objective",
                    ),
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl(dmc.Title("Dashboard", order=4, fw="normal")),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Text(
                                        "The dashboard provides interactive visualizations of aggregate data from all "
                                        "assessment submissions, offering insights into attachment style patterns across "
                                        "different demographics."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text("Available Visualizations", fw="bold", c=constants.PRIMARY),
                                    dmc.List([
                                        dmc.ListItem(
                                            dmc.Text(
                                                "Box Plots: Show distribution of attachment scores by demographic groups "
                                                "(age, gender, relationship status, therapy experience)")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text(
                                                "Scatter Plots: Explore relationships between different attachment dimensions")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text(
                                                "3D Scatter Plot: Visualize all three attachment dimensions simultaneously")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text(
                                                "Parallel Coordinates: Explore the correlation between different demographic variables")
                                        ),
                                    ]),
                                    dmc.Space(h="md"),
                                    dmc.Text("Dashboard Features", fw="bold", c=constants.PRIMARY),
                                    dmc.List([
                                        dmc.ListItem(
                                            dmc.Text("Filter data by assessment type (Self vs. Others)")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Include or exclude test submissions")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Real-time KPIs showing sample size and dominant patterns")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Interactive charts that respond to user selections")
                                        ),
                                    ]),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        "All visualizations update dynamically based on your filter selections, "
                                        "allowing for detailed exploration of how attachment styles vary across "
                                        "different populations and contexts"
                                    ),
                                ]
                            )
                        ],
                        value="dashboard",
                    ),
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl(dmc.Title("Technology", order=4, fw="normal")),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Text(
                                        "This application is built entirely in Python, demonstrating the capabilities "
                                        "of modern Python web frameworks for creating interactive psychological assessments."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text("Tech Stack", fw="bold", c=constants.PRIMARY),
                                    dmc.List([
                                        dmc.ListItem(
                                            dmc.Text("Frontend: Dash Plotly with Dash Mantine Components for UI")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Backend: Flask (underlying Dash framework)")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Database: PostgreSQL with SQLAlchemy ORM")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Data Processing: NumPy and Pandas for calculations")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Visualizations: Plotly for interactive charts")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text(
                                                "Deployment: Docker containers with database migrations via Alembic")
                                        ),
                                    ]),
                                    dmc.Space(h="md"),
                                    dmc.Text("Key Features", fw="bold", c=constants.PRIMARY),
                                    dmc.List([
                                        dmc.ListItem(
                                            dmc.Text("PDF generation for downloadable results")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Real-time dashboard with aggregate statistics")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Responsive design that works on all devices")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Interactive visualizations for exploring results")
                                        ),
                                    ]),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        "This project serves as both a functional psychological assessment tool and "
                                        "a demonstration of Python's capabilities for building full-stack web applications "
                                        "without traditional HTML/CSS/JavaScript development."
                                    ),
                                ]
                            )
                        ],
                        value="technology",
                    ),
                ],
            )
        ]
    )
