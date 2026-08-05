"""
Flashcard Service — Topic-aware mock AI flashcard generation.

Generates enriched flashcards with question, answer, hint, difficulty, and tags.
When a specific topic is provided (e.g. from a Day node), generates targeted cards.
Otherwise falls back to whole-course generation.

To upgrade to real LLM: replace _generate_topic_flashcards() with an OpenAI call.
"""

import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.utils.session_store import session_store


# ── Topic-specific flashcard templates ──────────────────────────────

TOPIC_FLASHCARDS = {
    "python": [
        {"question": "What is a variable in Python?", "answer": "A named container that stores a value in memory. Created using assignment: x = 10", "hint": "Think of it as a labeled box", "difficulty": "easy", "tags": ["python", "basics", "variables"]},
        {"question": "What is the difference between a list and a tuple?", "answer": "Lists are mutable (can be changed) while tuples are immutable (cannot be changed after creation).", "hint": "One uses [] and the other uses ()", "difficulty": "medium", "tags": ["python", "data-structures"]},
        {"question": "What does the 'def' keyword do?", "answer": "It defines a new function. Syntax: def function_name(parameters):", "hint": "Short for 'define'", "difficulty": "easy", "tags": ["python", "functions"]},
        {"question": "What is a dictionary in Python?", "answer": "An unordered collection of key-value pairs. Created using curly braces: {'key': 'value'}", "hint": "Like a real dictionary — look up a word (key) to find its meaning (value)", "difficulty": "easy", "tags": ["python", "data-structures"]},
        {"question": "What is list comprehension?", "answer": "A concise way to create lists: [expression for item in iterable if condition]. Example: [x**2 for x in range(5)]", "hint": "One-liner for loops that build lists", "difficulty": "medium", "tags": ["python", "lists", "comprehension"]},
        {"question": "What does 'self' refer to in a Python class?", "answer": "It refers to the current instance of the class, allowing access to its attributes and methods.", "hint": "The object talking about itself", "difficulty": "medium", "tags": ["python", "oop", "classes"]},
        {"question": "What is the purpose of __init__ in a class?", "answer": "It is the constructor method that initializes a new object's attributes when the class is instantiated.", "hint": "Runs automatically when you create an object", "difficulty": "medium", "tags": ["python", "oop", "constructor"]},
        {"question": "What is a lambda function?", "answer": "An anonymous, single-expression function. Syntax: lambda args: expression. Example: square = lambda x: x**2", "hint": "A function without a name", "difficulty": "hard", "tags": ["python", "functions", "lambda"]},
    ],
    "string": [
        {"question": "How do you find the length of a string?", "answer": "Use the len() function: len('hello') returns 5", "hint": "A built-in function that counts", "difficulty": "easy", "tags": ["python", "strings", "built-in"]},
        {"question": "What does the .strip() method do?", "answer": "Removes leading and trailing whitespace from a string.", "hint": "Cleaning up spaces at the edges", "difficulty": "easy", "tags": ["python", "strings", "methods"]},
        {"question": "How do you convert a string to uppercase?", "answer": "Use the .upper() method: 'hello'.upper() returns 'HELLO'", "hint": "The opposite of .lower()", "difficulty": "easy", "tags": ["python", "strings"]},
        {"question": "What is string slicing?", "answer": "Extracting a portion of a string using indices: s[start:end:step]. Example: 'hello'[1:4] returns 'ell'", "hint": "Like cutting a piece from a loaf", "difficulty": "medium", "tags": ["python", "strings", "slicing"]},
        {"question": "What are f-strings?", "answer": "Formatted string literals (Python 3.6+) that allow embedding expressions: f'Hello {name}'", "hint": "The f before the quote", "difficulty": "medium", "tags": ["python", "strings", "formatting"]},
        {"question": "Are strings mutable or immutable in Python?", "answer": "Strings are immutable — you cannot change individual characters after creation.", "hint": "You must create a new string instead", "difficulty": "medium", "tags": ["python", "strings", "immutability"]},
    ],
    "loop": [
        {"question": "What is the difference between 'for' and 'while' loops?", "answer": "'for' iterates over a sequence, 'while' repeats as long as a condition is True.", "hint": "One is count-based, the other is condition-based", "difficulty": "easy", "tags": ["python", "loops"]},
        {"question": "What does the 'break' statement do?", "answer": "It immediately exits the current loop, skipping any remaining iterations.", "hint": "Emergency exit from the loop", "difficulty": "easy", "tags": ["python", "loops", "control-flow"]},
        {"question": "What does 'continue' do in a loop?", "answer": "It skips the rest of the current iteration and jumps to the next one.", "hint": "Skip this one, move to next", "difficulty": "easy", "tags": ["python", "loops", "control-flow"]},
        {"question": "What does range(5) generate?", "answer": "A sequence of numbers: 0, 1, 2, 3, 4 (starts at 0, stops before 5).", "hint": "It doesn't include the stop value", "difficulty": "easy", "tags": ["python", "loops", "range"]},
        {"question": "What is a nested loop?", "answer": "A loop inside another loop. The inner loop completes all iterations for each iteration of the outer loop.", "hint": "Loop inception", "difficulty": "medium", "tags": ["python", "loops", "nested"]},
        {"question": "What does enumerate() do?", "answer": "Returns both the index and value during iteration: for i, val in enumerate(list).", "hint": "When you need the position AND the item", "difficulty": "medium", "tags": ["python", "loops", "enumerate"]},
    ],
    "function": [
        {"question": "What is a function parameter vs argument?", "answer": "Parameters are variables in the function definition. Arguments are actual values passed when calling the function.", "hint": "Definition vs call", "difficulty": "medium", "tags": ["python", "functions"]},
        {"question": "What is a return value?", "answer": "The value a function sends back to the caller using the 'return' statement.", "hint": "The function's output", "difficulty": "easy", "tags": ["python", "functions", "return"]},
        {"question": "What happens if a function has no return statement?", "answer": "It returns None by default.", "hint": "Python's version of 'nothing'", "difficulty": "easy", "tags": ["python", "functions"]},
        {"question": "What are *args and **kwargs?", "answer": "*args collects extra positional arguments as a tuple. **kwargs collects extra keyword arguments as a dictionary.", "hint": "Variable-length argument lists", "difficulty": "hard", "tags": ["python", "functions", "advanced"]},
        {"question": "What is a default parameter?", "answer": "A parameter with a pre-assigned value: def greet(name='World'). Used when no argument is provided.", "hint": "The fallback value", "difficulty": "easy", "tags": ["python", "functions", "defaults"]},
    ],
    "web": [
        {"question": "What does HTML stand for?", "answer": "HyperText Markup Language — the standard language for creating web pages.", "hint": "It's about structure, not style", "difficulty": "easy", "tags": ["web", "html"]},
        {"question": "What is the CSS box model?", "answer": "Every element is a box with: content → padding → border → margin (from inside out).", "hint": "Like layers of an onion", "difficulty": "medium", "tags": ["web", "css", "layout"]},
        {"question": "What is the DOM?", "answer": "Document Object Model — a tree representation of the HTML document that JavaScript can manipulate.", "hint": "The browser's internal structure of your page", "difficulty": "medium", "tags": ["web", "javascript", "dom"]},
        {"question": "What is the difference between GET and POST?", "answer": "GET requests data from a server (read-only). POST sends data to a server (creates/modifies).", "hint": "Reading vs writing", "difficulty": "medium", "tags": ["web", "http", "api"]},
        {"question": "What is responsive design?", "answer": "An approach that makes web pages render well on all devices using flexible layouts, media queries, and fluid grids.", "hint": "One design, many screen sizes", "difficulty": "easy", "tags": ["web", "css", "responsive"]},
    ],
}

# Fallback generic flashcards
GENERIC_FLASHCARDS = [
    {"question": "What are the key learning objectives of this topic?", "answer": "Understanding core concepts, applying principles to practical scenarios, and building foundational knowledge for advanced topics.", "hint": "Think about what you should know after studying", "difficulty": "easy", "tags": ["general", "learning"]},
    {"question": "How does this topic relate to the broader subject?", "answer": "It provides foundational building blocks that connect to more advanced concepts and real-world applications.", "hint": "Think connections and dependencies", "difficulty": "medium", "tags": ["general", "context"]},
    {"question": "What are common mistakes beginners make with this topic?", "answer": "Confusing similar concepts, skipping fundamentals, and not practicing with hands-on exercises.", "hint": "Learn from others' errors", "difficulty": "easy", "tags": ["general", "tips"]},
    {"question": "How would you explain this topic to a beginner?", "answer": "Start with a real-world analogy, then introduce the formal definition, and finally show a practical example.", "hint": "Analogy → Definition → Example", "difficulty": "medium", "tags": ["general", "teaching"]},
    {"question": "What practical applications does this topic have?", "answer": "This topic is used in software development, data analysis, automation, and problem-solving across many industries.", "hint": "Where is this used in the real world?", "difficulty": "easy", "tags": ["general", "applications"]},
]


def generate_flashcards(
    session_id: str,
    topic: Optional[str] = None,
    difficulty: Optional[str] = "beginner"
) -> Dict[str, Any]:
    """
    Generate flashcards, optionally filtered by topic.

    Args:
        session_id: Session identifier
        topic: Optional specific topic (e.g. "Python Strings")
        difficulty: Difficulty level filter

    Returns:
        Dictionary with success status and enriched flashcards
    """
    try:
        # Validate session exists
        session_data = session_store.get_session(session_id)
        if not session_data:
            return {
                "success": False,
                "message": "Session not found or expired"
            }

        # Generate flashcards
        flashcards = _generate_topic_flashcards(topic, difficulty)

        return {
            "success": True,
            "flashcards": flashcards,
            "topic": topic,
            "generated_at": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating flashcards: {str(e)}"
        }


def _generate_topic_flashcards(
    topic: Optional[str],
    difficulty: Optional[str] = "beginner"
) -> List[Dict[str, Any]]:
    """
    Generate topic-specific flashcards by matching topic keywords
    against the template bank.

    In production, replace this with an actual LLM call.
    """
    if not topic:
        return GENERIC_FLASHCARDS[:5]

    topic_lower = topic.lower()
    matched = []

    # Match against topic keyword banks
    for keyword, cards in TOPIC_FLASHCARDS.items():
        if keyword in topic_lower:
            matched.extend(cards)

    # If no specific match, try broader matching
    if not matched:
        # Check if any topic keyword appears in the input
        for keyword, cards in TOPIC_FLASHCARDS.items():
            if any(word in topic_lower for word in keyword.split()):
                matched.extend(cards[:3])

    # Still nothing? Use generic + topic-customized
    if not matched:
        matched = [
            {
                "question": f"What is {topic}?",
                "answer": f"{topic} is a key concept in this course that covers fundamental principles and practical applications.",
                "hint": "Start with the definition",
                "difficulty": "easy",
                "tags": [topic.lower().replace(" ", "-"), "definition"]
            },
            {
                "question": f"Why is {topic} important to learn?",
                "answer": f"Understanding {topic} is essential because it forms the foundation for more advanced concepts and is widely used in practice.",
                "hint": "Think real-world relevance",
                "difficulty": "easy",
                "tags": [topic.lower().replace(" ", "-"), "importance"]
            },
            {
                "question": f"What are the core components of {topic}?",
                "answer": f"{topic} consists of several interconnected elements including theory, practical application, and problem-solving strategies.",
                "hint": "Break it into parts",
                "difficulty": "medium",
                "tags": [topic.lower().replace(" ", "-"), "components"]
            },
            {
                "question": f"How do you apply {topic} in a real project?",
                "answer": f"Start by understanding the fundamentals, then practice with small exercises, and finally integrate {topic} into a complete project.",
                "hint": "Theory → Practice → Integration",
                "difficulty": "medium",
                "tags": [topic.lower().replace(" ", "-"), "application"]
            },
            {
                "question": f"What are common pitfalls when working with {topic}?",
                "answer": f"Common mistakes include skipping fundamentals, not testing enough, and over-complicating solutions. Always start simple.",
                "hint": "Learn from mistakes",
                "difficulty": "easy",
                "tags": [topic.lower().replace(" ", "-"), "tips"]
            },
        ]

    # Filter by difficulty if specified
    if difficulty and difficulty != "beginner":
        diff_map = {"intermediate": ["medium", "hard"], "advanced": ["hard"]}
        allowed = diff_map.get(difficulty, ["easy", "medium", "hard"])
        filtered = [c for c in matched if c.get("difficulty") in allowed]
        if filtered:
            matched = filtered

    # Limit to 5-8 cards
    return matched[:8]