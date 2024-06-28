from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

top_margin = 0.5 * 72
bottom_margin = 150
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
chart = Image("../data/figure.png", width=700/2, height=500/2)
story.append(chart)
# Create a Paragraph and append it to the story
description_text = """
    Anxious: You love to be very close to your romantic partners and have the capacity 
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
description = Paragraph(description_text, styles["Normal"])
story.append(description)
# Building the story into the document template
doc.build(story)
