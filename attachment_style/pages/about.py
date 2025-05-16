from dash import register_page, dcc
import dash_bootstrap_components as dbc

register_page(__name__)


def layout(**kwargs):
    return dbc.Container(
        dcc.Markdown(
            """
            This app is inspired by the book Attached Book by Amir Levine and Rachel S. F. Heller and uses the questionnaires and texts from the book.
            It is also a personal coding exercise. I wanted to see if one can use Dash Plotly
            to build a full-fledged interactive website without any html or javascript - in pure
            Python. The code can be found at https://github.com/kotenevmatvei/attachment-style.
            
            The main advantages of this quiz compared to others that may be found on the internet are:
            
            - The opportunity to download a pdf of the final report with all the questions and answers. It can be
            used as a conversation starter for someone struggling in a relationship.
            - The option to be more differentiated in your answers - on the scale from 0 to 10 instead of the standard
            "strongly disagree" to "neutral" to "strongly agree".
            - A more practical, behaviour-based questionnaire with examples that can be completed with regard to someone 
            else, for example your partner.
            - Dashboard visualizing the global results in different plots.
            
            """
        ),
    )
