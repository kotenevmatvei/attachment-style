from dash import register_page
import dash_mantine_components as dmc

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
                            dmc.AccordionControl("Assess Yourself"),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Text(
                                        "The 'Assess Yourself' quiz is based on the ECR-R (Experiences in Close Relationships-Revised) scale, "
                                        "a scientifically validated instrument for measuring adult attachment styles in romantic relationships."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        "This assessment consists of 36 questions divided into two dimensions:"
                                    ),
                                    dmc.List([
                                        dmc.ListItem(
                                            dmc.Text("Anxious Attachment (18 questions): Measures fear of abandonment, "
                                                   "need for reassurance, and worry about relationships")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Avoidant Attachment (18 questions): Measures discomfort with closeness, "
                                                   "preference for independence, and difficulty with emotional intimacy")
                                        ),
                                    ]),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        "Your responses help determine your primary attachment style: Secure, Anxious, or Avoidant. "
                                        "The ECR-R is widely used in psychological research and provides reliable insights into "
                                        "how you approach close relationships."
                                    ),
                                ]
                            )
                        ],
                        value="assess-yourself",
                    ),
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl("Assess Others (ECR-R)"),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Text(
                                        "The 'Assess Others' feature uses a modified version of the ECR-R scale adapted for "
                                        "evaluating the attachment behaviors of other people in your life - such as romantic "
                                        "partners, friends, or family members."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        "This assessment includes 33 questions across three dimensions:"
                                    ),
                                    dmc.List([
                                        dmc.ListItem(
                                            dmc.Text("Anxious behaviors (11 questions): Observable signs of relationship anxiety "
                                                   "and fear of abandonment in others")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Avoidant behaviors (11 questions): Observable signs of emotional distance "
                                                   "and discomfort with intimacy in others")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Secure behaviors (11 questions): Observable signs of healthy relationship "
                                                   "patterns and emotional availability in others")
                                        ),
                                    ]),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        "This tool helps you better understand the attachment patterns of people around you, "
                                        "which can improve communication and relationship dynamics. The questions focus on "
                                        "observable behaviors rather than internal feelings."
                                    ),
                                ]
                            )
                        ],
                        value="assess-others",
                    ),
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl("Scoring"),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Text(
                                        "Our scoring system is based on established psychological research and provides "
                                        "nuanced insights into attachment patterns:"
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Title("ECR-R Scoring (Assess Yourself)", order=4, c=constants.PRIMARY),
                                    dmc.List([
                                        dmc.ListItem(
                                            dmc.Text("Questions are rated on a 7-point scale (1 = strongly disagree, 7 = strongly agree)")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Reverse-coded items (marked with /r/) are automatically adjusted")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Anxious and Avoidant scores are calculated as averages of their respective items")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Secure score is mathematically derived from the other two dimensions using: "
                                                   "Secure = 4 + ((4 - Anxious) + (4 - Avoidant)) / 2")
                                        ),
                                    ]),
                                    dmc.Space(h="md"),
                                    dmc.Title("Assess Others Scoring", order=4, c=constants.PRIMARY),
                                    dmc.List([
                                        dmc.ListItem(
                                            dmc.Text("Also uses a 7-point rating scale")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Includes direct measurement of secure behaviors")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Each dimension (Anxious, Avoidant, Secure) is scored independently")
                                        ),
                                    ]),
                                    dmc.Space(h="md"),
                                    dmc.Text(
                                        "Higher scores indicate stronger tendencies toward that attachment style. "
                                        "Your primary attachment style is determined by your highest score, but most "
                                        "people show elements of multiple styles."
                                    ),
                                ]
                            )
                        ],
                        value="scoring",
                    ),
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl("Technology"),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Text(
                                        "This application is built entirely in Python, demonstrating the capabilities "
                                        "of modern Python web frameworks for creating interactive psychological assessments."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Title("Tech Stack", order=4, c=constants.PRIMARY),
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
                                            dmc.Text("Deployment: Docker containers with database migrations via Alembic")
                                        ),
                                    ]),
                                    dmc.Space(h="md"),
                                    dmc.Title("Key Features", order=4, c=constants.PRIMARY),
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
                                            dmc.Text("Secure data storage with privacy protection")
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
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl("Dashboard"),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Text(
                                        "The dashboard provides interactive visualizations of aggregate data from all "
                                        "assessment submissions, offering insights into attachment style patterns across "
                                        "different demographics."
                                    ),
                                    dmc.Space(h="md"),
                                    dmc.Title("Available Visualizations", order=4, c=constants.PRIMARY),
                                    dmc.List([
                                        dmc.ListItem(
                                            dmc.Text("Box Plots: Show distribution of attachment scores by demographic groups "
                                                   "(age, gender, relationship status, therapy experience)")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Scatter Plots: Explore relationships between different attachment dimensions")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("3D Scatter Plot: Visualize all three attachment dimensions simultaneously")
                                        ),
                                        dmc.ListItem(
                                            dmc.Text("Parallel Coordinates: Compare attachment profiles across multiple dimensions")
                                        ),
                                    ]),
                                    dmc.Space(h="md"),
                                    dmc.Title("Dashboard Features", order=4, c=constants.PRIMARY),
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
                                        "different populations and contexts. The dashboard respects user privacy "
                                        "by only showing aggregate, anonymized data."
                                    ),
                                ]
                            )
                        ],
                        value="dashboard",
                    ),
                ],
            )
        ]
    )