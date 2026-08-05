"""
Course Generation Prompt — all prompt text for course generation lives here.

Design decisions:
    • System message defines the AI's role and hard constraints.
    • Human message contains the parameterised request and the JSON schema.
    • Schema is defined as a readable docstring, not generated from Pydantic,
      because the LLM needs natural-language guidance alongside the structure.
    • No prompt strings should exist in llm_service.py — they all live here.
"""

from langchain_core.prompts import ChatPromptTemplate


# ──────────────────────────────────────────────────────────────
# System prompt — defines the AI persona and output constraints
# ──────────────────────────────────────────────────────────────

COURSE_SYSTEM_PROMPT = """\
You are an expert curriculum designer and educator with deep knowledge \
across technology, science, business, and the humanities.

Your task is to generate a complete, structured, production-quality course.

HARD RULES:
1. Return ONLY valid JSON — no markdown fences, no explanatory text, \
no comments, no trailing commas.
2. Every string value must be properly escaped.
3. Follow the exact field names and types specified in the schema.
4. Content must be educational, accurate, and actionable.
5. Each day's content MUST be 150-250 words of rich educational material \
using markdown formatting (## headers, **bold**, bullet points, numbered lists). \
Do NOT exceed 300 words per day — be concise but thorough.
6. All assignments must have both questions AND solutions.
7. All flashcards must have a front (question/term) and back (answer/explanation).
8. The JSON response MUST be COMPLETE. Include ALL weeks, ALL days, ALL \
assignments, and ALL flashcards in a single valid JSON object. \
Do NOT truncate or abbreviate the output. Ensure the final closing brace is present.\
"""


# ──────────────────────────────────────────────────────────────
# JSON schema — communicated to the LLM as part of the prompt
# ──────────────────────────────────────────────────────────────

COURSE_JSON_SCHEMA = """\
{{
  "title":               "string — descriptive course title that includes the topic name",
  "description":         "string — 2-3 sentence course overview",
  "learning_objectives": ["string — 4 to 8 specific, measurable learning outcomes"],
  "prerequisites":       ["string — 2 to 4 prerequisite knowledge items"],
  "weeks": [
    {{
      "week_number": "integer — 1-indexed, sequential",
      "title":       "string — thematic title for the week",
      "objectives":  ["string — exactly 3 learning objectives for this week"],
      "days": [
        {{
          "day_number":  "integer — 1 to 5",
          "title":       "string — topic title for the day",
          "objectives":  ["string — 2 to 3 learning objectives"],
          "content":     "string — detailed educational content (≥150 words, use markdown)",
          "activities":  ["string — 3 to 4 practical learning activities"]
        }}
      ]
    }}
  ],
  "assignments": [
    {{
      "title":      "string — assignment title",
      "type":       "string — one of: MCQ, coding, theory",
      "difficulty": "string — must match course difficulty level",
      "questions":  ["string — 3 assessment questions"],
      "solutions":  ["string — corresponding model answers"]
    }}
  ],
  "flashcards": [
    {{
      "front":    "string — question or key term",
      "back":     "string — answer or detailed explanation",
      "category": "string — one of: Concept, Syntax, Practice, Theory"
    }}
  ]
}}\
"""


# ──────────────────────────────────────────────────────────────
# Human prompt — parameterised with topic, duration, etc.
# ──────────────────────────────────────────────────────────────

COURSE_HUMAN_PROMPT = """\
Generate a complete **{difficulty}**-level course on **"{topic}"** \
in **{language}**, spanning **{duration} weeks**.

REQUIREMENTS:
• Generate exactly {duration} weeks, each with exactly 5 days.
• Each day's "content" field must contain at least 150 words of rich, \
original educational material with markdown formatting.
• Include 2 to 3 assignments of mixed types (MCQ, coding, theory).
• Include 4 to 6 flashcards covering the most important concepts.
• Ensure a logical, progressive learning path from week 1 to week {duration}.
• Tailor depth and vocabulary to the **{difficulty}** level.
• Write all content in **{language}**.

OUTPUT SCHEMA (return ONLY this JSON, nothing else):

{schema}\
"""


def get_course_prompt() -> ChatPromptTemplate:
    """
    Build and return the ChatPromptTemplate for course generation.

    The template expects these input variables at invocation time:
        topic      — str
        duration   — int
        difficulty — str
        language   — str

    The schema variable is injected automatically.
    """
    return ChatPromptTemplate.from_messages([
        ("system", COURSE_SYSTEM_PROMPT),
        ("human", COURSE_HUMAN_PROMPT),
    ]).partial(schema=COURSE_JSON_SCHEMA)
