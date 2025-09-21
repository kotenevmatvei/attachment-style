from dash import callback, Output, Input, State
import smtplib
from email.mime.text import MIMEText


def send_email(subject, message, to_email):
    email = "kotenev.matvei@gmail.com"
    password = "gqtc afhx miac yxka "

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
    Output("dummy-email-div", "children"),
    Input("send-feedback-button", "n_clicks"),
    [
        State("feedback-input", "value"),
        State("email-input", "value"),
    ],
    prevent_initial_call=True,
)
def send_feedback(n_clicks, feedback, email):
    send_email("AST FEEDBACK", feedback + f"\nemail: {email}", "kotenev.matvei@gmail.com")


