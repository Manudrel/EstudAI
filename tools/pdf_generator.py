from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def markdown_to_pdf(title, content):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 12),
        Paragraph(
            content.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    ]

    doc.build(elements)

    buffer.seek(0)

    return buffer