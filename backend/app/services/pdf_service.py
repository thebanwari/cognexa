# import os
# import markdown
# from jinja2 import Environment, FileSystemLoader
# from typing import Dict, Any, Optional
# from datetime import datetime
# import logging
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import inch

# logger = logging.getLogger(__name__)


# def course_json_to_markdown(course_data: Dict[str, Any]) -> str:
#     """
#     Convert course JSON data to Markdown format.

#     Args:
#         course_data: Course data as dictionary

#     Returns:
#         Markdown content as string
#     """
#     try:
#         # Load template
#         template_dir = "app/templates"
#         env = Environment(loader=FileSystemLoader(template_dir))
#         template = env.get_template("course_template.md")

#         # Render markdown
#         markdown_content = template.render(
#             course=course_data,
#             generated_date=datetime.now().strftime("%B %d, %Y")
#         )

#         logger.info("Successfully converted course JSON to Markdown")
#         return markdown_content

#     except Exception as e:
#         logger.error(f"Failed to convert course JSON to Markdown: {e}")
#         # Fallback to basic markdown generation
#         return _fallback_markdown_generation(course_data)


# def _fallback_markdown_generation(course_data: Dict[str, Any]) -> str:
#     """Fallback method to generate markdown from course data"""
#     lines = []

#     # Course title and metadata
#     lines.append(f"# {course_data.get('title', 'Course')}")
#     lines.append("")
#     lines.append(f"**Description:** {course_data.get('description', '')}")
#     lines.append(f"**Difficulty:** {course_data.get('difficulty', 'N/A')}")
#     lines.append(f"**Duration:** {course_data.get('duration_weeks', 0)} weeks")
#     lines.append(f"**Language:** {course_data.get('language', 'English')}")
#     lines.append("")

#     # Learning objectives
#     objectives = course_data.get('learning_objectives', [])
#     if objectives:
#         lines.append("## Learning Objectives")
#         for obj in objectives:
#             lines.append(f"- {obj}")
#         lines.append("")

#     # Prerequisites
#     prerequisites = course_data.get('prerequisites', [])
#     if prerequisites:
#         lines.append("## Prerequisites")
#         for prereq in prerequisites:
#             lines.append(f"- {prereq}")
#         lines.append("")

#     # Weeks
#     weeks = course_data.get('weeks', [])
#     for week in weeks:
#         week_num = week.get('week_number', 0)
#         week_title = week.get('title', f'Week {week_num}')
#         lines.append(f"## Week {week_num}: {week_title}")

#         week_objectives = week.get('objectives', [])
#         if week_objectives:
#             lines.append("**Objectives:**")
#             for obj in week_objectives:
#                 lines.append(f"- {obj}")

#         # Days
#         days = week.get('days', [])
#         for day in days:
#             day_num = day.get('day_number', 0)
#             day_title = day.get('title', f'Day {day_num}')
#             lines.append(f"### Day {day_num}: {day_title}")

#             day_objectives = day.get('objectives', [])
#             if day_objectives:
#                 lines.append("**Objectives:**")
#                 for obj in day_objectives:
#                     lines.append(f"- {obj}")

#             day_content = day.get('content', '')
#             if day_content:
#                 lines.append("**Content:**")
#                 lines.append(day_content)

#             day_activities = day.get('activities', [])
#             if day_activities:
#                 lines.append("**Activities:**")
#                 for activity in day_activities:
#                     lines.append(f"- {activity}")

#             lines.append("")

#     # Assignments
#     assignments = course_data.get('assignments', [])
#     if assignments:
#         lines.append("## Assignments")
#         for assignment in assignments:
#             title = assignment.get('title', 'Assignment')
#             type_ = assignment.get('type', 'N/A')
#             difficulty = assignment.get('difficulty', 'N/A')
#             lines.append(f"### {title}")
#             lines.append(f"**Type:** {type_}")
#             lines.append(f"**Difficulty:** {difficulty}")

#             questions = assignment.get('questions', [])
#             if questions:
#                 lines.append("**Questions:**")
#                 for i, question in enumerate(questions, 1):
#                     lines.append(f"{i}. {question}")

#             lines.append("")

#     # Flashcards
#     flashcards = course_data.get('flashcards', [])
#     if flashcards:
#         lines.append("## Flashcards")
#         for flashcard in flashcards:
#             front = flashcard.get('front', '')
#             back = flashcard.get('back', '')
#             category = flashcard.get('category', '')
#             lines.append(f"### {front} ({category})")
#             lines.append(back)
#             lines.append("")

#     return "\n".join(lines)


# def markdown_to_html(markdown_content: str) -> str:
#     """
#     Convert Markdown to HTML.

#     Args:
#         markdown_content: Markdown content

#     Returns:
#         HTML content as string
#     """
#     try:
#         # Convert markdown to HTML
#         html_content = markdown.markdown(
#             markdown_content,
#             extensions=['fenced_code', 'codehilite', 'tables', 'sane_lists']
#         )

#         # Add CSS styling
#         styled_html = _add_css_styling(html_content)

#         logger.info("Successfully converted Markdown to HTML")
#         return styled_html

#     except Exception as e:
#         logger.error(f"Failed to convert Markdown to HTML: {e}")
#         return f"<html><body><pre>{markdown_content}</pre></body></html>"


# def _add_css_styling(html_content: str) -> str:
#     """Add CSS styling to HTML content"""
#     css = """
#     <style>
#         body {
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#             line-height: 1.6;
#             color: #333;
#             max-width: 800px;
#             margin: 0 auto;
#             padding: 20px;
#             background-color: #fafafa;
#         }
#         h1, h2, h3, h4, h5, h6 {
#             color: #2c3e50;
#             margin-top: 1.5em;
#             margin-bottom: 0.5em;
#         }
#         h1 {
#             border-bottom: 3px solid #3498db;
#             padding-bottom: 10px;
#         }
#         h2 {
#             border-bottom: 2px solid #2ecc71;
#             padding-bottom: 8px;
#         }
#         code {
#             background-color: #ecf0f1;
#             padding: 2px 4px;
#             border-radius: 3px;
#             font-family: 'Courier New', monospace;
#         }
#         pre {
#             background-color: #2c3e50;
#             color: #ecf0f1;
#             padding: 15px;
#             border-radius: 5px;
#             overflow-x: auto;
#             font-family: 'Courier New', monospace;
#             line-height: 1.4;
#         }
#         pre code {
#             background-color: transparent;
#             color: inherit;
#             padding: 0;
#         }
#         ul, ol {
#             padding-left: 20px;
#         }
#         li {
#             margin-bottom: 8px;
#         }
#         table {
#             border-collapse: collapse;
#             width: 100%;
#             margin: 15px 0;
#         }
#         th, td {
#             border: 1px solid #ddd;
#             padding: 12px;
#             text-align: left;
#         }
#         th {
#             background-color: #3498db;
#             color: white;
#         }
#         tr:nth-child(even) {
#             background-color: #f2f2f2;
#         }
#         .course-meta {
#             background-color: #e8f4fd;
#             border-left: 4px solid #3498db;
#             padding: 15px;
#             margin: 20px 0;
#         }
#         .learning-objectives {
#             background-color: #e8f5e8;
#             border-left: 4px solid #2ecc71;
#             padding: 15px;
#             margin: 20px 0;
#         }
#         .prerequisites {
#             background-color: #fff3cd;
#             border-left: 4px solid #ffc107;
#             padding: 15px;
#             margin: 20px 0;
#         }
#         .footer {
#             margin-top: 40px;
#             padding-top: 20px;
#             border-top: 1px solid #ddd;
#             text-align: center;
#             color: #777;
#             font-size: 0.9em;
#         }
#     </style>
#     """

#     return f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <meta charset="UTF-8">
#         <title>{_extract_title_from_html(html_content) or 'Course Content'}</title>
#         {css}
#     </head>
#     <body>
#         {html_content}
#         <div class="footer">
#             <p>Generated by CourseCraft-AI on {datetime.now().strftime("%B %d, %Y")}</p>
#         </div>
#     </body>
#     </html>
#     """


# def _extract_title_from_html(html_content: str) -> Optional[str]:
#     """Extract title from HTML content"""
#     import re
#     title_match = re.search(r'<h1>(.*?)</h1>', html_content)
#     if title_match:
#         return title_match.group(1)
#     return None


# def save_pdf_file(html_content: str, file_path: str) -> bool:
#     """
#     Windows-safe PDF generator using ReportLab.
#     HTML content is converted to plain text paragraphs.
#     """

#     try:
#         doc = SimpleDocTemplate(
#             file_path,
#             pagesize=letter,
#             rightMargin=40,
#             leftMargin=40,
#             topMargin=40,
#             bottomMargin=40
#         )

#         styles = getSampleStyleSheet()
#         story = []

#         # Basic title extraction
#         title = "Course PDF"
#         if "<h1>" in html_content:
#             try:
#                 title = html_content.split("<h1>")[1].split("</h1>")[0]
#             except Exception:
#                 pass

#         story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
#         story.append(Spacer(1, 0.2 * inch))

#         # Remove raw HTML tags to convert to clean text
#         import re
#         clean_text = re.sub('<[^<]+?>', '', html_content)

#         # Split paragraphs
#         paragraphs = clean_text.split("\n")

#         for para in paragraphs:
#             if para.strip() != "":
#                 story.append(Paragraph(para.strip(), styles["BodyText"]))
#                 story.append(Spacer(1, 0.15 * inch))

#         doc.build(story)
#         return True

#     except Exception as e:
#         logger.error(f"ReportLab PDF generation failed: {e}")
#         return False


# def generate_course_pdf(course_data: Dict[str, Any], output_path: str) -> bool:
#     """
#     Generate PDF from course data using Markdown → HTML → ReportLab.
#     Fully Windows-safe.
#     """
#     try:
#         # Convert JSON → Markdown
#         markdown_content = course_json_to_markdown(course_data)
#         if not markdown_content:
#             logger.error("Failed to generate Markdown from course data")
#             return False

#         # Convert Markdown → HTML
#         html_content = markdown_to_html(markdown_content)
#         if not html_content:
#             logger.error("Failed to generate HTML from Markdown")
#             return False

#         # Save PDF using Windows-safe ReportLab
#         success = save_pdf_file(html_content, output_path)

#         if success:
#             logger.info(f"PDF generated: {output_path}")
#         else:
#             logger.error(f"PDF generation failed for: {output_path}")

#         return success

#     except Exception as e:
#         logger.error(f"Error in generate_course_pdf: {e}")
#         return False


import os
import re
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


# ---------------------------
# MARKDOWN → REPORTLAB PARSER
# ---------------------------

def parse_markdown_to_story(markdown_text: str):
    styles = getSampleStyleSheet()

    # Custom styles (more bold and clear)
    styles.add(ParagraphStyle(name='H1', parent=styles['Heading1'], fontSize=22, spaceAfter=12))
    styles.add(ParagraphStyle(name='H2', parent=styles['Heading2'], fontSize=18, spaceAfter=10))
    styles.add(ParagraphStyle(name='H3', parent=styles['Heading3'], fontSize=14, spaceAfter=8))
    styles.add(ParagraphStyle(name='CustomBullet', parent=styles['BodyText'], leftIndent=20, bulletIndent=10))
    styles.add(ParagraphStyle(name='NormalText', parent=styles['BodyText'], fontSize=11, spaceAfter=6))

    lines = markdown_text.split("\n")
    story = []

    bullet_buffer = []  # For collecting bullet points

    for line in lines:
        stripped = line.strip()

        # H1
        if stripped.startswith("# "):
            if bullet_buffer:
                story.append(make_bullet_list(bullet_buffer, styles))
                bullet_buffer = []
            story.append(Paragraph(stripped[2:], styles['H1']))
            story.append(Spacer(1, 0.1 * inch))

        # H2
        elif stripped.startswith("## "):
            if bullet_buffer:
                story.append(make_bullet_list(bullet_buffer, styles))
                bullet_buffer = []
            story.append(Paragraph(stripped[3:], styles['H2']))
            story.append(Spacer(1, 0.1 * inch))

        # H3
        elif stripped.startswith("### "):
            if bullet_buffer:
                story.append(make_bullet_list(bullet_buffer, styles))
                bullet_buffer = []
            story.append(Paragraph(stripped[4:], styles['H3']))
            story.append(Spacer(1, 0.05 * inch))

        # Bullet point
        elif stripped.startswith("- "):
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
            story.append(Paragraph(stripped, styles['NormalText']))

    # Flush remaining bullets
    if bullet_buffer:
        story.append(make_bullet_list(bullet_buffer, styles))

    return story


def make_bullet_list(bullets, styles):
    return ListFlowable(
        [ListItem(Paragraph(b, styles['CustomBullet'])) for b in bullets],
        bulletType='bullet'
)



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
    