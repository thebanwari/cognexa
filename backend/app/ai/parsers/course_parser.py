"""
Course JSON Parser — extracts, cleans, and validates the LLM's JSON output.

Design decisions:
    • The parser is intentionally lenient on extraction (handles markdown fences,
      leading/trailing junk) but strict on schema validation.
    • Validation is done by constructing Pydantic models from course_models.py,
      which ensures the output matches the exact contract the rest of the app expects.
    • If validation fails, a clear CourseParsingError is raised so the chain
      can retry with a fresh LLM call.
"""

import json
import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class CourseParsingError(Exception):
    """Raised when the LLM output cannot be parsed into a valid course dict."""
    pass


def parse_course_json(raw_output: str) -> Dict[str, Any]:
    """
    Parse raw LLM text output into a validated course dictionary.

    Steps:
        1. Extract JSON string from the raw output (handles code fences).
        2. Parse into a Python dict.
        3. Validate required top-level keys.
        4. Validate nested structure (weeks → days, assignments, flashcards).
        5. Normalise any minor issues (missing optional fields, type coercion).

    Args:
        raw_output: The raw text returned by the LLM.

    Returns:
        A validated course dictionary matching the mock_llm_course_generator schema.

    Raises:
        CourseParsingError: If extraction, parsing, or validation fails.
    """
    # ── Step 1: Extract JSON string ─────────────────────────────
    json_str = _extract_json(raw_output)

    # ── Step 2: Repair common LLM JSON defects ──────────────────
    json_str = _repair_json(json_str)

    # ── Step 3: Parse JSON ──────────────────────────────────────
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise CourseParsingError(f"Invalid JSON: {e}")

    if not isinstance(data, dict):
        raise CourseParsingError(
            f"Expected a JSON object at root level, got {type(data).__name__}"
        )

    # ── Step 4: Validate top-level keys ─────────────────────────
    _validate_top_level(data)

    # ── Step 5: Validate nested structures ──────────────────────
    _validate_weeks(data.get("weeks", []))
    _validate_assignments(data.get("assignments", []))
    _validate_flashcards(data.get("flashcards", []))

    # ── Step 6: Normalise ───────────────────────────────────────
    data = _normalise(data)

    logger.info(
        f"Successfully parsed course: {data.get('title', 'Untitled')} "
        f"({len(data.get('weeks', []))} weeks, "
        f"{len(data.get('assignments', []))} assignments, "
        f"{len(data.get('flashcards', []))} flashcards)"
    )
    return data


# ─────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────

def _extract_json(text: str) -> str:
    """
    Extract a JSON object string from potentially noisy LLM output.

    Uses brace-depth tracking with string-awareness to find the
    outermost { ... } pair.  This correctly handles triple-backtick
    code fences, markdown fences wrapping the response, and any
    embedded code blocks inside JSON string values.

    Handles:
        • Raw JSON (starts with {)
        • JSON wrapped in ```json ... ``` fences
        • Leading/trailing prose before/after the JSON object
    """
    text = text.strip()

    # Find the first opening brace
    brace_start = text.find("{")
    if brace_start == -1:
        raise CourseParsingError("No JSON object found in LLM output")

    # Walk forward to find the matching closing brace
    depth = 0
    in_string = False
    escape_next = False
    for i in range(brace_start, len(text)):
        char = text[i]
        if escape_next:
            escape_next = False
            continue
        if char == "\\":
            escape_next = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[brace_start:i + 1]

    # If we get here, braces are unbalanced — return what we have
    return text[brace_start:]



def _repair_json(text: str) -> str:
    """
    Fix common LLM JSON defects that cause json.loads() to fail.

    Primary fix: literal newlines / tabs / control characters inside
    JSON string values.  JSON requires these to be escaped (\\n, \\t)
    but LLMs routinely emit the raw characters when generating
    multiline content such as markdown.

    Algorithm:
        Walk the string character-by-character, tracking whether we
        are inside a JSON string (between unescaped double-quotes).
        When inside a string, replace illegal control characters with
        their JSON escape sequences.
    """
    result = []
    in_string = False
    i = 0
    length = len(text)

    while i < length:
        char = text[i]

        if char == '\\' and in_string and i + 1 < length:
            # Already-escaped sequence — keep both characters as-is
            result.append(char)
            result.append(text[i + 1])
            i += 2
            continue

        if char == '"':
            in_string = not in_string
            result.append(char)
            i += 1
            continue

        if in_string:
            # Replace control characters that are illegal inside JSON strings
            if char == '\n':
                result.append('\\n')
            elif char == '\r':
                result.append('\\r')
            elif char == '\t':
                result.append('\\t')
            elif ord(char) < 0x20:
                # Other control chars → Unicode escape
                result.append(f'\\u{ord(char):04x}')
            else:
                result.append(char)
        else:
            result.append(char)

        i += 1

    return ''.join(result)


REQUIRED_TOP_LEVEL_KEYS = {
    "title", "description", "learning_objectives", "prerequisites",
    "weeks", "assignments", "flashcards",
}


def _validate_top_level(data: Dict[str, Any]) -> None:
    """Check that all required top-level keys are present."""
    missing = REQUIRED_TOP_LEVEL_KEYS - set(data.keys())
    if missing:
        raise CourseParsingError(f"Missing required top-level keys: {missing}")

    if not isinstance(data["weeks"], list) or len(data["weeks"]) == 0:
        raise CourseParsingError("'weeks' must be a non-empty list")

    if not isinstance(data["learning_objectives"], list):
        raise CourseParsingError("'learning_objectives' must be a list")

    if not isinstance(data["prerequisites"], list):
        raise CourseParsingError("'prerequisites' must be a list")


def _validate_weeks(weeks: List[Dict]) -> None:
    """Validate each week and its nested days."""
    for i, week in enumerate(weeks):
        if not isinstance(week, dict):
            raise CourseParsingError(f"Week {i} is not a dict")

        for key in ("week_number", "title", "objectives", "days"):
            if key not in week:
                raise CourseParsingError(
                    f"Week {i} missing required key: '{key}'"
                )

        days = week.get("days", [])
        if not isinstance(days, list) or len(days) == 0:
            raise CourseParsingError(
                f"Week {i} 'days' must be a non-empty list"
            )

        for j, day in enumerate(days):
            if not isinstance(day, dict):
                raise CourseParsingError(
                    f"Week {i}, Day {j} is not a dict"
                )
            for key in ("day_number", "title", "objectives", "content", "activities"):
                if key not in day:
                    raise CourseParsingError(
                        f"Week {i}, Day {j} missing required key: '{key}'"
                    )


def _validate_assignments(assignments: List[Dict]) -> None:
    """Validate each assignment."""
    for i, assign in enumerate(assignments):
        if not isinstance(assign, dict):
            raise CourseParsingError(f"Assignment {i} is not a dict")

        for key in ("title", "type", "difficulty", "questions"):
            if key not in assign:
                raise CourseParsingError(
                    f"Assignment {i} missing required key: '{key}'"
                )


def _validate_flashcards(flashcards: List[Dict]) -> None:
    """Validate each flashcard."""
    for i, card in enumerate(flashcards):
        if not isinstance(card, dict):
            raise CourseParsingError(f"Flashcard {i} is not a dict")

        for key in ("front", "back", "category"):
            if key not in card:
                raise CourseParsingError(
                    f"Flashcard {i} missing required key: '{key}'"
                )


def _normalise(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fix minor issues that don't warrant a full retry:
        • Ensure week_number and day_number are ints
        • Add empty 'solutions' to assignments if missing
        • Add empty 'resources' to days if missing
    """
    for week in data.get("weeks", []):
        week["week_number"] = int(week.get("week_number", 0))
        week["objectives"] = list(week.get("objectives", []))
        for day in week.get("days", []):
            day["day_number"] = int(day.get("day_number", 0))
            day["objectives"] = list(day.get("objectives", []))
            day["activities"] = list(day.get("activities", []))
            if "resources" not in day:
                day["resources"] = []

    for assign in data.get("assignments", []):
        if "solutions" not in assign:
            assign["solutions"] = []

    return data
