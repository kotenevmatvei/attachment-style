from dash import register_page, html, dcc
import dash_bootstrap_components as dbc

register_page(__name__)


def layout(**kwargs):
    return dbc.Container(
        dcc.Markdown(
            """
            This test is mainly a personal coding exercise. It has been inspired by Amir Levine's book 
            [*"Attached: The New Science of Adult Attachment  and How It Can Help You Find - and Keep - Love"*]
            (https://www.amazon.de/-/en/Attached-Science-Attachment-Find-Keep-Love/dp/1585429139), which I highly
            recommend if you are interested in learning more about the attachment style theory. 
            
            The main advantages of this quiz compared to others that may be found on the internet are:
            
            - The opportunity to download a pdf of the final report with all the questions and answers. It can be
            used a conversation starter for someone struggling in a relationship.
            - The option to be more differentiated in your answers - on the scale from 0 to 10 instead of the standard
            "strongly disagree" to "neutral" to "strongly agree".
            - A more practical, behaviour-based questionnaire with examples that can be completed with regard to someone 
            else, for example your partner.
            
            Future functionality may include a dashboard presenting the results of the test over different age groups,
            genders etc. For this, the data is already collected anonymously in a database.
            """
        ),
    )
