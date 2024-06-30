from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from plotly.express import pie


def generate_report(answers: dict[str, tuple[str, float, str]]) -> None:
    top_margin = 0.5 * 72
    # Create a SimpleDocTemplate
    doc = SimpleDocTemplate("data/report.pdf", topMargin=top_margin)
    # Fetch the built-in styles, and return a list to append elements to
    styles = getSampleStyleSheet()
    story = []
    # create a title
    title = Paragraph("Attachment Style Report", styles["Title"])
    story.append(title)
    # add space
    story.append(Spacer(0, 10))
    # add chart
    chart = Image("data/figure.png", width=700 / 2, height=500 / 2)
    story.append(chart)
    # add a horizontal ruler to divide next section
    story.append(HRFlowable(width="90%", thickness=1, lineCap='round', spaceBefore=15, spaceAfter=10, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    # write anxious description
    anxious_description_text = """
        <b>Anxious</b>: You love to be very close to your romantic partners and have the capacity 
        for great intimacy. You often fear, however, that your partner does not wish to be as 
        close as you would like him/her to be. Relationships tend to consume a large part of 
        your emotional energy. You tend to be very sensitive to small fluctuations in your 
        partner’s moods and actions, and although your senses are often accurate, you take 
        your partner’s behaviors too personally. You experience a lot of negative emotions 
        within the relationship and get easily upset. As a result, you tend to act out and 
        say things you later regret. If the other person provides a lot of security and 
        reassurance, however, you are able to shed much of your preoccupation and feel 
        contented.
    """
    secure_description = Paragraph(anxious_description_text, styles["Normal"])
    story.append(secure_description)
    story.append(Spacer(0, 10))
    # write secure description
    secure_description_text = """
        <b>Secure</b>: Being warm and loving in a relationship comes naturally to you. You 
        enjoy being intimate without becoming overly worried about your relationships. 
        You take things in stride when it comes to romance and don’t get easily upset 
        over relationship matters. You effectively communicate your needs and feelings 
        to your partner and are strong at reading your partner’s emotional cues and 
        responding to them. You share your successes and problems with your mate, and 
        are able to be there for him or her in times of need.
    """
    secure_description = Paragraph(secure_description_text, styles["Normal"])
    story.append(secure_description)
    story.append(Spacer(0, 10))
    avoidant_description_text = """
        <b>Avoidant</b>: It is very important for you to maintain your independence and 
        self-sufficiency and you often prefer autonomy to intimate relationships. Even 
        though you do want to be close to others, you feel uncomfortable with too much 
        closeness and tend to keep your partner at arm’s length. You don’t spend much 
        time  worrying about your romantic relationships or about being rejected. You 
        tend not to open up to your partners and they often complain that you are 
        emotionally distant. In relationships, you are often on high alert for any signs 
        of control or impingement on your territory by your partner.
    """
    avoidant_description = Paragraph(avoidant_description_text, styles["Normal"])
    story.append(avoidant_description)

    # add a horizontal ruler to divide next section
    story.append(HRFlowable(width="90%", thickness=1, lineCap='round', spaceBefore=15, spaceAfter=10, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    # add anxious Q&A
    centered = ParagraphStyle(name="Centered", parent=styles['Heading3'], alignment=1)
    story.append(Paragraph("Your Answers:", centered))
    story.append(Paragraph("<b>Anxious</b>:"))
    anxious_answers = [(value[2], value[1]) for value in answers.values() if value[0] == "anxious"]
    print(answers)
    for answer in anxious_answers:
        question = Paragraph(answer[0], styles["Normal"])
        story.append(question)
        answer_text = f"Answer: {answer[1]}"
        answer_paragraph = Paragraph(answer_text, styles["Normal"])
        story.append(answer_paragraph)
        story.append(Spacer(0, 5))
    # add secure answers
    story.append(Paragraph("<b>Secure</b>:"))
    anxious_answers = [(value[2], value[1]) for value in answers.values() if value[0] == "secure"]
    for answer in anxious_answers:
        question = Paragraph(answer[0], styles["Normal"])
        story.append(question)
        answer_text = f"Answer: {answer[1]}"
        answer_paragraph = Paragraph(answer_text, styles["Normal"])
        story.append(answer_paragraph)
        story.append(Spacer(0, 5))
    # add avoidant answers
    story.append(Paragraph("<b>Avoidant</b>:"))
    anxious_answers = [(value[2], value[1]) for value in answers.values() if value[0] == "avoidant"]
    for answer in anxious_answers:
        question = Paragraph(answer[0], styles["Normal"])
        story.append(question)
        answer_text = f"Answer: {answer[1]}"
        answer_paragraph = Paragraph(answer_text, styles["Normal"])
        story.append(answer_paragraph)
        story.append(Spacer(0, 5))
    # Building the story into the document template
    doc.build(story)