import re
from typing import List


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100) -> List[str]:
    """
    Split text into chunks of specified size with overlap.

    Args:
        text: Input text to chunk
        chunk_size: Target size for each chunk (in characters)
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if not text or len(text) <= chunk_size:
        return [text] if text else []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If we're not at the end, try to break at a sentence boundary
        if end < len(text):
            # Look for sentence endings (.!?) in the last 100 characters
            search_start = max(start + chunk_size - 100, start)
            sentence_end = -1

            for pattern in [r'[.!?]\s+', r'\.\s+', r'!\s+', r'?\s+', r'\n\n', r'\n']:
                matches = list(re.finditer(pattern, text[search_start:end]))
                if matches:
                    sentence_end = search_start + matches[-1].end()

            # If we found a good break point, use it
            if sentence_end > start + chunk_size // 2:
                end = sentence_end
            else:
                # Otherwise, break at a word boundary
                last_space = text.rfind(' ', start + chunk_size - 50, start + chunk_size)
                if last_space > start:
                    end = last_space

        chunk = text[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)

        # Move to next chunk, considering overlap
        start = end - overlap
        if start >= len(text):
            break

    return chunks


def chunk_course_content(course_text: str) -> List[str]:
    """
    Specialized chunking for course content that respects section boundaries.

    Args:
        course_text: Full course content as a string

    Returns:
        List of course chunks
    """
    # Split by major sections (Weeks, Days)
    sections = re.split(r'\n(Week \d+:|Day \d+:)', course_text)

    chunks = []
    current_chunk = ""

    for i in range(0, len(sections), 2):
        if i + 1 < len(sections):
            section_header = sections[i + 1]
            section_content = sections[i + 2] if i + 2 < len(sections) else ""
            section_text = f"{section_header}{section_content}"
        else:
            section_text = sections[i]

        # If section is too big, chunk it further
        if len(section_text) > 1000:
            # First try to add current chunk if it exists
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            # Chunk the large section
            section_chunks = chunk_text(section_text, chunk_size=700, overlap=100)
            chunks.extend(section_chunks)
        else:
            # Add section to current chunk
            if len(current_chunk + section_text) > 700 and current_chunk:
                chunks.append(current_chunk)
                current_chunk = section_text
            else:
                current_chunk += "\n" + section_text if current_chunk else section_text

    # Add remaining content
    if current_chunk:
        chunks.append(current_chunk)

    # Ensure no chunk is too small (unless it's the only one)
    if len(chunks) > 1:
        merged_chunks = []
        i = 0
        while i < len(chunks):
            chunk = chunks[i]
            if len(chunk) < 200 and i < len(chunks) - 1:
                # Merge with next chunk
                chunk += "\n\n" + chunks[i + 1]
                i += 1
            merged_chunks.append(chunk)
            i += 1
        chunks = merged_chunks

    return chunks