import re
import html
from typing import List


def clean_text(text: str) -> str:
    """
    Clean and normalize text for better processing.

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # HTML unescape
    text = html.unescape(text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.

    Args:
        text: Input text

    Returns:
        Text with normalized whitespace
    """
    if not text:
        return ""

    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)

    # Replace multiple newlines with double newlines
    text = re.sub(r'\n+', '\n\n', text)

    # Replace tabs with spaces
    text = text.replace('\t', ' ')

    return text.strip()


def sanitize_for_filename(text: str) -> str:
    """
    Sanitize text for use in filenames.

    Args:
        text: Input text

    Returns:
        Sanitized filename
    """
    if not text:
        return "course"

    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', text)

    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')

    # Remove multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)

    # Limit length
    sanitized = sanitized[:100]

    # Ensure it's not empty
    if not sanitized:
        sanitized = "course"

    return sanitized


def extract_key_phrases(text: str, max_phrases: int = 10) -> List[str]:
    """
    Extract key phrases from text (simple implementation).

    Args:
        text: Input text
        max_phrases: Maximum number of phrases to return

    Returns:
        List of key phrases
    """
    if not text:
        return []

    # Simple approach: split by sentences and take meaningful ones
    sentences = re.split(r'[.!?]+', text)
    meaningful_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 10 and any(c.isalpha() for c in sentence):
            meaningful_sentences.append(sentence)

    return meaningful_sentences[:max_phrases]


def format_course_content(content: str) -> str:
    """
    Format course content for better readability.

    Args:
        content: Raw course content

    Returns:
        Formatted content
    """
    if not content:
        return ""

    # Clean the content
    content = clean_text(content)

    # Add proper spacing around headings
    content = re.sub(r'\n([A-Z][A-Z\s]+)\n', r'\n\n**\1**\n\n', content)

    # Format lists
    content = re.sub(r'\n(\d+\.\s)', r'\n\1', content)
    content = re.sub(r'\n(-\s)', r'\n\1', content)

    # Ensure proper paragraph spacing
    content = re.sub(r'\n([^\n])', r'\n\n\1', content)

    return content.strip()


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add when truncating

    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text

    # Find a good break point (try to break at word boundary)
    truncate_point = max_length - len(suffix)

    if truncate_point <= 0:
        return suffix

    # Look for space before the truncate point
    space_pos = text.rfind(' ', 0, truncate_point)

    if space_pos > max_length * 0.8:  # Break at space if it's not too far back
        return text[:space_pos].strip() + suffix
    else:
        return text[:truncate_point].strip() + suffix