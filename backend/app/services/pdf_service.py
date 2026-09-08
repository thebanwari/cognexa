import os
import re
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    Preformatted,
    Flowable,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class BackgroundPreformatted(Flowable):
    """Preformatted text with a visible background rectangle.

    ReportLab's Preformatted.draw() ignores ParagraphStyle.backColor,
    so this wrapper draws the background rect manually before
    delegating text rendering to a standard Preformatted flowable.

    Split strategy:
        - If the block fits on a fresh page, defer it entirely.
        - If splitting is unavoidable, keep at least _MIN_SPLIT_LINES
          on each side to prevent orphaned fragments.
    """

    _PADDING = 8  # points of padding inside the background rect
    _MIN_SPLIT_LINES = 3  # minimum lines to keep on either side of a split

    def __init__(self, text, style):
        super().__init__()
        self._pre = Preformatted(text, style)
        self._bg = style.backColor
        self._style = style

    def wrap(self, availWidth, availHeight):
        w, h = self._pre.wrap(availWidth, availHeight)
        self.width = w
        self.height = h + 2 * self._PADDING
        return self.width, self.height

    def split(self, availWidth, availHeight):
        usable = availHeight - 2 * self._PADDING
        leading = self._style.leading
        total_lines = len(self._pre.lines)

        # How many lines fit in the available space?
        lines_that_fit = int(usable / leading)

        # Nothing fits — defer to the next page
        if lines_that_fit < self._MIN_SPLIT_LINES:
            return []

        # Everything fits — no split needed
        if lines_that_fit >= total_lines:
            return [self]

        lines_remaining = total_lines - lines_that_fit

        # The remainder is a small orphan AND the whole block would
        # fit on a fresh page (~57 lines at leading=12) — defer entirely
        full_page_lines = int(692.0 / leading)  # 692pt usable on letter
        if lines_remaining <= self._MIN_SPLIT_LINES and total_lines <= full_page_lines:
            return []

        # If splitting would leave too few lines on the first page,
        # also defer (block fits on next page)
        if lines_that_fit < self._MIN_SPLIT_LINES and total_lines <= full_page_lines:
            return []

        # Genuine split — block is too large for one page
        text1 = "\n".join(self._pre.lines[:lines_that_fit])
        text2 = "\n".join(self._pre.lines[lines_that_fit:])
        return [
            BackgroundPreformatted(text1, self._style),
            BackgroundPreformatted(text2, self._style),
        ]

    def draw(self):
        if self._bg:
            self.canv.saveState()
            self.canv.setFillColor(self._bg)
            self.canv.rect(
                0, 0, self.width, self.height,
                stroke=0, fill=1,
            )
            self.canv.restoreState()
        self._pre.drawOn(self.canv, 0, self._PADDING)


# ---------------------------
# MARKDOWN → REPORTLAB PARSER
# ---------------------------

def md_to_rl(text: str) -> str:
    """Convert inline markdown syntax to ReportLab XML tags.

    Handles:
        **bold**   → <b>bold</b>
        *italic*   → <i>italic</i>
        `code`     → <font name="Courier" color="#c0392b">code</font>

    Asterisks inside code spans (e.g. `*args`, `**kwargs`) are escaped
    so they are not misinterpreted as bold/italic markers.
    """
    # Code spans first — escape asterisks inside the matched content
    # so the bold/italic passes don't corrupt code like *args / **kwargs
    def _code_span(m):
        inner = m.group(1).replace("*", "&#42;")
        return f'<font name="Courier" color="#c0392b">{inner}</font>'

    text = re.sub(r'`([^`]+?)`', _code_span, text)
    # Bold (**text**) — must come before italic
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic (*text*) — only single asterisks remaining after bold pass
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    return text


def parse_markdown_to_story(markdown_text: str):
    styles = getSampleStyleSheet()

    # Custom styles — keepWithNext prevents orphan headings at page bottoms
    styles.add(ParagraphStyle(name='H1', parent=styles['Heading1'], fontSize=22, spaceAfter=12, keepWithNext=True))
    styles.add(ParagraphStyle(name='H2', parent=styles['Heading2'], fontSize=18, spaceAfter=10, keepWithNext=True))
    styles.add(ParagraphStyle(name='H3', parent=styles['Heading3'], fontSize=14, spaceAfter=8, keepWithNext=True))
    styles.add(ParagraphStyle(name='CustomBullet', parent=styles['BodyText'], leftIndent=20, bulletIndent=10))
    styles.add(ParagraphStyle(name='NormalText', parent=styles['BodyText'], fontSize=11, spaceAfter=6))
    styles.add(ParagraphStyle(
        name='CodeBlock',
        fontName='Courier',
        fontSize=9,
        leading=12,
        leftIndent=10,
        rightIndent=10,
        spaceBefore=8,
        spaceAfter=8,
        backColor=HexColor('#2c3e50'),
        textColor=HexColor('#ecf0f1'),
    ))

    lines = markdown_text.split("\n")
    story = []

    bullet_buffer = []  # For collecting bullet points
    in_code_block = False
    code_buffer = []  # For collecting code block lines

    for line in lines:
        stripped = line.strip()

        # ── Fenced code block handling ──────────────────────
        if stripped.startswith("```"):
            if not in_code_block:
                # Opening fence — flush any pending bullets, enter code mode
                if bullet_buffer:
                    story.append(make_bullet_list(bullet_buffer, styles))
                    bullet_buffer = []
                in_code_block = True
                code_buffer = []
                continue  # skip the opening ``` line
            else:
                # Closing fence — emit the collected code block
                code_text = "\n".join(code_buffer)
                story.append(BackgroundPreformatted(code_text, styles['CodeBlock']))
                in_code_block = False
                code_buffer = []
                continue  # skip the closing ``` line

        if in_code_block:
            # Preserve the original line (including leading whitespace)
            code_buffer.append(line.rstrip())
            continue

        # ── Normal markdown handling ─────────────────────────
        # Heading order: check #### before ### before ## before #

        # H4 (rendered as H3 — no separate visual level needed)
        if stripped.startswith("#### "):
            if bullet_buffer:
                story.append(make_bullet_list(bullet_buffer, styles))
                bullet_buffer = []
            story.append(Paragraph(md_to_rl(stripped[5:]), styles['H3']))

        # H3
        elif stripped.startswith("### "):
            if bullet_buffer:
                story.append(make_bullet_list(bullet_buffer, styles))
                bullet_buffer = []
            story.append(Paragraph(md_to_rl(stripped[4:]), styles['H3']))

        # H2
        elif stripped.startswith("## "):
            if bullet_buffer:
                story.append(make_bullet_list(bullet_buffer, styles))
                bullet_buffer = []
            story.append(Paragraph(md_to_rl(stripped[3:]), styles['H2']))

        # H1
        elif stripped.startswith("# "):
            if bullet_buffer:
                story.append(make_bullet_list(bullet_buffer, styles))
                bullet_buffer = []
            story.append(Paragraph(md_to_rl(stripped[2:]), styles['H1']))

        # Bullet point (- item or * item)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            bullet_buffer.append(stripped[2:])

        # Numbered list
        elif re.match(r"^\d+\.", stripped):
            bullet_buffer.append(stripped)

        # Empty line = paragraph break
        elif stripped == "":
            if bullet_buffer:
                story.append(make_bullet_list(bullet_buffer, styles))
                bullet_buffer = []
            story.append(Spacer(1, 0.15 * inch))

        # Normal paragraph
        else:
            if bullet_buffer:
                story.append(make_bullet_list(bullet_buffer, styles))
                bullet_buffer = []
            story.append(Paragraph(md_to_rl(stripped), styles['NormalText']))

    # Flush remaining buffers
    if in_code_block and code_buffer:
        # Unclosed code block — emit what we have
        code_text = "\n".join(code_buffer)
        story.append(BackgroundPreformatted(code_text, styles['CodeBlock']))
    if bullet_buffer:
        story.append(make_bullet_list(bullet_buffer, styles))

    # Post-process: wrap each heading + its first following flowable
    # in KeepTogether to reliably prevent orphan headings.
    story = _keep_headings_with_content(story)

    return story


def make_bullet_list(bullets, styles):
    return ListFlowable(
        [ListItem(Paragraph(md_to_rl(b), styles['CustomBullet'])) for b in bullets],
        bulletType='bullet'
    )


_HEADING_STYLES = frozenset(('H1', 'H2', 'H3'))


def _keep_headings_with_content(story):
    """Wrap each heading + its first following content flowable in KeepTogether.

    This prevents orphan headings at page bottoms more reliably than
    keepWithNext alone.  Spacers between heading and content are included
    in the group so they don't break the bond.
    """
    result = []
    i = 0
    while i < len(story):
        flowable = story[i]

        # Check if this is a heading Paragraph
        is_heading = (
            isinstance(flowable, Paragraph)
            and hasattr(flowable, 'style')
            and flowable.style.name in _HEADING_STYLES
        )

        if is_heading and i + 1 < len(story):
            # Collect heading + any spacers + first content flowable
            group = [flowable]
            j = i + 1
            # Skip spacers (include them in the group)
            while j < len(story) and isinstance(story[j], Spacer):
                group.append(story[j])
                j += 1
            # Include the first content flowable after the spacers
            if j < len(story):
                group.append(story[j])
                j += 1
            result.append(KeepTogether(group))
            i = j
        else:
            result.append(flowable)
            i += 1

    return result


# ------------------------
# COURSE → MARKDOWN FORMAT
# ------------------------

def course_to_markdown(course: Dict[str, Any]) -> str:
    md = []

    # Title
    md.append(f"# {course['title']}\n")

    md.append(f"**Description:** {course['description']}\n")
    md.append(f"**Difficulty:** {course['difficulty']}")
    md.append(f"**Duration:** {course['duration_weeks']} weeks\n")

    # Objectives
    md.append("## Learning Objectives")
    for obj in course['learning_objectives']:
        md.append(f"- {obj}")
    md.append("")

    # Weeks
    for week in course["weeks"]:
        md.append(f"## Week {week['week_number']}: {week['title']}")
        for day in week["days"]:
            md.append(f"### Day {day['day_number']}: {day['title']}")
            md.append(day["content"])
            md.append("")

    # Assignments
    md.append("## Assignments")
    for assign in course.get("assignments", []):
        md.append(f"### {assign['title']}")
        for q in assign["questions"]:
            md.append(f"- {q}")
        md.append("")

    # Flashcards
    md.append("## Flashcards")
    for card in course.get("flashcards", []):
        md.append(f"### {card['front']}")
        md.append(f"- {card['back']}")
        md.append("")

    return "\n".join(md)


# ------------------------
# GENERATE FINAL PDF
# ------------------------

def generate_course_pdf(course: Dict[str, Any], output_path: str) -> bool:
    try:
        markdown_text = course_to_markdown(course)

        story = parse_markdown_to_story(markdown_text)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            leftMargin=50,
            rightMargin=50,
            topMargin=50,
            bottomMargin=50
        )

        doc.build(story)
        return True

    except Exception as e:
        print("PDF Generation Error:", e)
        return False