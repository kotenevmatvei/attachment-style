import logging
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Image,
    Spacer,
    HRFlowable,
    Table,
    Indenter,
)

logger = logging.getLogger(__name__)


def generate_report(answers: dict[str, dict], dominant_style) -> None:
    top_margin = 0.75 * 72
    doc = SimpleDocTemplate(
        "tmp/attachment_style_report.pdf",
        topMargin=top_margin,
        leftMargin=0.75 * 72,
        rightMargin=0.75 * 72,
        bottomMargin=0.75 * 72,
    )
    styles = getSampleStyleSheet()
    # Custom styles
    subtitle_style = ParagraphStyle(
        name="Subtitle",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#2B2D42"),
        spaceAfter=6,
        alignment=1,
    )
    section_header = ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading3"],
        textColor=colors.HexColor("#1D3557"),
        spaceBefore=12,
        spaceAfter=6,
    )
    normal_style = ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        leading=15,
    )
    bullet_style = ParagraphStyle(
        name="Bullet",
        parent=styles["BodyText"],
        leftIndent=14,
        bulletIndent=4,
        spaceBefore=2,
        spaceAfter=2,
    )

    story = []
    # Title
    # Make a single title with the subtitle's visual style, centered at the top
    story.append(Paragraph("Your attachment style report", subtitle_style))
    story.append(Spacer(0, 12))

    # Chart (prefer 'figure_you.png' if available by context; fall back handled by caller saving file)
    chart = Image("tmp/figure.png", width=440, height=315)
    story.append(chart)

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            lineCap="round",
            spaceBefore=15,
            spaceAfter=10,
            hAlign="CENTER",
            vAlign="BOTTOM",
        )
    )

    # Build style descriptions using the same wording as results_callbacks.py
    # We don't import Dash components; we rephrase them as plain text.
    def style_block(name: str, text: str, bullets: list[str]):
        # Keep headings with the first paragraph to reduce awkward page breaks
        section_header.keepWithNext = True
        story.append(Paragraph(f"<b>{name}</b>", section_header))
        story.append(Paragraph(text, normal_style))
        if bullets:
            for b in bullets:
                story.append(Paragraph(f"• {b}", bullet_style))
        story.append(Spacer(0, 8))

    # Texts adapted from results_callbacks.update_dominant_style_text
    anxious_text = (
        "People with an anxious attachment style tend to crave emotional intimacy but often "
        "feel insecure and doubtful about their partner's love and commitment. They may have "
        "a negative self-view and a positive view of their partners, leading to a deep-seated "
        "fear of abandonment. This anxiety can cause them to seek constant reassurance, over-"
        "analyze their partner's behavior, and become highly dependent on the relationship "
        "for their sense of self-worth."
    )
    anxious_bullets = [
        "Intense craving for closeness and intimacy",
        "Persistent worry about the partner's love and the relationship's stability",
        "Tendency to be emotionally dependent on the partner",
        "High sensitivity to a partner's moods and actions",
        "Fear of being alone or rejected",
    ]

    secure_text = (
        "People with a secure attachment style typically feel comfortable with intimacy and are "
        "usually warm and loving. They have a positive view of themselves and their partners. "
        "They communicate effectively, are comfortable depending on others and having others "
        "depend on them, and don't worry about being alone or being accepted."
    )
    secure_bullets = [
        "Comfortable with emotional intimacy",
        "Effective communication skills",
        "Balanced need for independence and closeness",
        "Positive self-image and view of others",
        "Resilient in handling relationship conflicts",
    ]

    avoidant_text = (
        "People with an avoidant attachment style are often highly independent and self-"
        "sufficient, preferring to handle problems on their own. They tend to be uncomfortable "
        "with emotional closeness and may suppress their feelings to avoid intimacy. While they "
        "may have a positive self-image, they can be dismissive of others' needs for closeness and "
        "may view partners as overly demanding. They prioritize their freedom and may distance "
        "themselves when they feel a partner is getting too close."
    )
    avoidant_bullets = [
        "Strong emphasis on independence and self-reliance",
        "Discomfort with emotional intimacy and sharing feelings",
        "Tendency to create distance in relationships",
        "Avoidance of dependency on others",
        "Suppression of emotional expression",
    ]

    style_block("Anxious", anxious_text, anxious_bullets)
    style_block("Secure", secure_text, secure_bullets)
    style_block("Avoidant", avoidant_text, avoidant_bullets)

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            lineCap="round",
            spaceBefore=15,
            spaceAfter=10,
            hAlign="CENTER",
            vAlign="BOTTOM",
        )
    )

    centered = ParagraphStyle(name="Centered", parent=styles["Heading3"], alignment=1)
    # Section: Your Answers (no forced page break)
    story.append(Paragraph("Your Answers:", centered))
    # add anxious answers
    story.append(Paragraph("<u><b>Anxious</b></u>:"))
    story.append(Spacer(0, 10))
    anxious_answers = {key: value for key, value in answers.items() if value and value["attachment_style"] == "anxious"}
    # sort anxious answers
    # anxious_answers = sorted(anxious_answers)
    data_anxious = []
    for key, answer in anxious_answers.items():
        # Convert markdown to HTML
        question = answer.get("question_text")

        question_title = question.get("title")
        header = Paragraph("<b>" + question_title + "</b>")

        question_bullet_points = question.get("bullet_points", [])
        indenter_on = Indenter(left=10)
        indenter_off = Indenter(left=-10)
        single_question = Paragraph("")
        bullet_points = []
        for point in question_bullet_points:
            bullet_points.append(Paragraph("\u2022" + point))
        question = [header, indenter_on, bullet_points, indenter_off]
        data_anxious.append([question, answer["score"]])
    # Add header row
    data_anxious.insert(0, [Paragraph("<b>Question / Rationale</b>", styles["BodyText"]),
                            Paragraph("<b>Score</b>", styles["BodyText"])])
    table_anxious = Table(
        data_anxious,
        colWidths=[400, 60],
        repeatRows=1,
        style=[
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFC0C0")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F3F5")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.Color(0.98, 0.98, 1)]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 1), (1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ],
    )
    story.append(table_anxious)

    # add secure answers
    if len(answers) == 33:
        story.append(Spacer(0, 10))
        story.append(Paragraph("<u><b>Secure</b></u>:"))
        story.append(Spacer(0, 10))
        secure_answers = {key: value for key, value in answers.items() if value and value["attachment_style"] == "secure"}
        # sort secure answers
        # secure_answers = sorted(secure_answers)
        data_secure = []
        for key, answer in secure_answers.items():
            # Convert markdown to HTML
            question = answer.get("question_text")

            question_title = question.get("title")
            header = Paragraph("<b>" + question_title + "</b>")

            question_bullet_points = question.get("bullet_points", [])
            indenter_on = Indenter(left=10)
            indenter_off = Indenter(left=-10)
            single_question = Paragraph("")
            bullet_points = []
            for point in question_bullet_points:
                bullet_points.append(Paragraph("\u2022" + point))
            question = [header, indenter_on, bullet_points, indenter_off]
            data_secure.append([question, answer["score"]])
        # Add header row
        data_secure.insert(0, [Paragraph("<b>Question / Rationale</b>", styles["BodyText"]),
                                Paragraph("<b>Score</b>", styles["BodyText"])])
        table_secure = Table(
            data_secure,
            colWidths=[400, 60],
            repeatRows=1,
            style=[
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFC0C0")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F3F5")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.Color(0.98, 0.98, 1)]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ],
        )
        story.append(table_secure)

    # add avoidant questions
    story.append(Spacer(0, 10))
    story.append(Paragraph("<u><b>Avoidant</b></u>:"))
    story.append(Spacer(0, 10))
    avoidant_answers = {key: value for key, value in answers.items() if value and value["attachment_style"] == "avoidant"}
    # sort avoidant answers
    # avoidant_answers = sorted(avoidant_answers)
    data_avoidant = []
    for key, answer in avoidant_answers.items():
        # Convert markdown to HTML
        question = answer.get("question_text")

        question_title = question.get("title")
        header = Paragraph("<b>" + question_title + "</b>")

        question_bullet_points = question.get("bullet_points", [])
        indenter_on = Indenter(left=10)
        indenter_off = Indenter(left=-10)
        single_question = Paragraph("")
        bullet_points = []
        for point in question_bullet_points:
            bullet_points.append(Paragraph("\u2022" + point))
        question = [header, indenter_on, bullet_points, indenter_off]
        data_avoidant.append([question, answer["score"]])
    # Add header row
    data_avoidant.insert(0, [Paragraph("<b>Question / Rationale</b>", styles["BodyText"]),
                            Paragraph("<b>Score</b>", styles["BodyText"])])
    table_avoidant = Table(
        data_avoidant,
        colWidths=[400, 60],
        repeatRows=1,
        style=[
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFC0C0")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F3F5")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.Color(0.98, 0.98, 1)]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 1), (1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ],
    )
    story.append(table_avoidant)

    # Next steps section based on dominant style
    # Encourage a page break before suggestions to avoid splitting tables and tips
    story.append(Spacer(0, 12))
    story.append(HRFlowable(width="100%", thickness=1, spaceBefore=10, spaceAfter=8))
    story.append(Paragraph("Suggestions to work on", section_header))

    suggestions = {
        "anxious": [
            "Mindset: Name the feeling ('I notice anxiety') and rate intensity (0–10)",
            "Practice: 4-7-8 breathing or body scan for 2–3 minutes",
            "Practice: Delay reassurance seeking by 10 minutes and journal your thought",
            "Conversation: Share needs using 'When X happens, I feel Y, I'd appreciate Z'",
            "Practice: Create a soothing playlist or anchor phrase for spikes",
            "Mindset: Reality-check stories; list 3 alternative explanations",
            "Practice: Schedule a weekly 'connection ritual' (walk, check-in questions)",
        ],
        "avoidant": [
            "Mindset: Notice the first urge to withdraw; label it without acting",
            "Practice: Share one small personal detail with a trusted person weekly",
            "Practice: Set a 10–15 min timer to stay present during discomfort",
            "Conversation: Express boundaries and needs instead of disappearing",
            "Practice: Plan low-pressure quality time that keeps autonomy (co-working, walks)",
            "Mindset: Reframe closeness as a skill-building experiment, not a trap",
            "Practice: Try 2-minute daily emotional check-in (What am I feeling? Why?)",
        ],
        "secure": [
            "Mindset: Maintain reflective listening in tough conversations",
            "Practice: Model repair attempts (own your part, propose a next step)",
            "Practice: Protect boundaries while staying warm and responsive",
            "Conversation: Invite feedback—'What helps you feel cared for with me?'",
            "Practice: Support partners with anxious/avoidant cues without over-functioning",
            "Mindset: Continue rituals of connection and appreciation",
        ],
    }

    story.append(Spacer(0, 4))
    story.append(Paragraph("These are gentle suggestions—try 1–2 for the next week and iterate.", normal_style))
    story.append(Spacer(0, 6))

    for tip in suggestions.get(dominant_style):
        story.append(Paragraph(f"• {tip}", bullet_style))

    story.append(Spacer(0, 10))
    story.append(Paragraph("Note: This report is informational and not a diagnosis.",
                           ParagraphStyle(name="Note", parent=styles["BodyText"],
                                          textColor=colors.HexColor("#495057"))))

    # build the PDF document with footer
    def _draw_footer(canvas, doc_):
        canvas.saveState()
        footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#6C757D"))
        canvas.drawRightString(doc_.pagesize[0] - doc_.rightMargin, 0.5 * 72 - 6, footer_text)
        canvas.restoreState()

    doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)
