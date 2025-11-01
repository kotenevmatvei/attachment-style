import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

from dash import callback, Output, Input, State, clientside_callback

load_dotenv()

def send_email(subject, message, to_email):
    email = "kotenev.matvei@gmail.com"
    password = os.getenv("GMAIL_APP_PASSWORD")

    # Create message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email, password)
        server.sendmail(email, to_email, msg.as_string())


@callback(
    [
        Output("thank-you-for-feedback-collapse", "opened"),
        Output("feedback-input", "error"),
        Output("email-input", "error"),
        Output("send-feedback-button", "loading", allow_duplicate=True),
    ],
    Input("send-feedback-button", "n_clicks"),
    [
        State("feedback-input", "value"),
        State("email-input", "value"),
    ],
    prevent_initial_call=True,
)
def send_feedback(n_clicks, feedback, email):
    if feedback and email:
        if "@" in email:
            message = feedback + f"\n\nemail: {email}"
            send_email("AST FEEDBACK", message, "kotenev.matvei@gmail.com")
        else: return False, None, "Please enter a valid email", False
    elif feedback:
        message = feedback
    else:
        return False, "Please fill the form", None, False

    if n_clicks == 1:
        send_email("AST FEEDBACK", message, "kotenev.matvei@gmail.com")
        return True, None, None, False
    elif n_clicks > 1:
        return True, None, None, False

    return False, None, None, False


# show loading while downloading the pdf report
clientside_callback(
    """
    function updateLoadingState(n_clicks) {
        return true
    }
    """,
    Output("send-feedback-button", "loading"),
    Input("send-feedback-button", "n_clicks"),
    prevent_initial_call=True,
)

# change page title order on mobile
@callback(
    Output("feedback-page-title", "order"),
    Input("window-width", "data"),
)
def resize_feedback_page_title(window_width):
    if window_width < 500:
        return 3
    return 1
