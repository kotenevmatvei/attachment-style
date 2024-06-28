from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from plotly.express import pie


top_margin = 0.5 * 72
# Create a SimpleDocTemplate
doc = SimpleDocTemplate("platypus_example.pdf", topMargin=top_margin)
# Fetch the built-in styles, and return a list to append elements to
styles = getSampleStyleSheet()
story = []
# create a title
title = Paragraph("Attachment Style Report", styles["Title"])
story.append(title)
# add space
story.append(Spacer(0, 10))
# add chart
chart = Image("../data/figure.png", width=700 / 2, height=500 / 2)
story.append(chart)
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
# Building the story into the document template
doc.build(story)

