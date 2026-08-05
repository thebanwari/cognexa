import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.models.course_models import Course, Week, Day, Assignment, Flashcard
from app.utils.text_cleaner import clean_text
from app.config import GEMINI_API_KEY, USE_MOCK_LLM

logger = logging.getLogger(__name__)

# ── Lazy singleton for the AI chain ─────────────────────────
_course_chain_instance = None


def _get_course_chain():
    """Lazy-initialise and cache the CourseChain singleton."""
    global _course_chain_instance
    if _course_chain_instance is None:
        from app.ai.chains.course_chain import CourseChain
        _course_chain_instance = CourseChain()
    return _course_chain_instance


def _should_use_ai() -> bool:
    """Determine whether to use real AI or fall back to mock."""
    if USE_MOCK_LLM:
        return False
    if not GEMINI_API_KEY:
        return False
    return True


# ═══════════════════════════════════════════════════════════════
# PUBLIC API — function name unchanged so routes are untouched
# ═══════════════════════════════════════════════════════════════

def mock_llm_course_generator(
    topic: str,
    duration: int = 4,
    difficulty: str = "beginner",
    language: str = "english"
) -> Dict[str, Any]:
    """
    Generate a complete course structure.

    Routing logic:
        • If GEMINI_API_KEY is set and USE_MOCK_LLM is False →
          uses the real LangChain + Gemini pipeline.
        • Otherwise (or on any AI failure) →
          falls back to the deterministic mock generator.

    The function signature and return schema are identical in both
    paths, so nothing downstream needs to change.

    Args:
        topic: Course topic
        duration: Duration in weeks
        difficulty: Difficulty level
        language: Language

    Returns:
        Course structure as dictionary
    """
    if _should_use_ai():
        try:
            logger.info(f"Using real AI for course generation: topic='{topic}'")
            return _generate_course_with_ai(topic, duration, difficulty, language)
        except Exception as e:
            logger.error(f"Gemini course generation failed: {e}")
            raise

    logger.info(f"Using mock generator for course generation: topic='{topic}'")
    return _mock_course_generator(topic, duration, difficulty, language)


# ═══════════════════════════════════════════════════════════════
# REAL AI PATH
# ═══════════════════════════════════════════════════════════════

def _generate_course_with_ai(
    topic: str,
    duration: int,
    difficulty: str,
    language: str,
) -> Dict[str, Any]:
    """
    Generate a course using the LangChain CourseChain (Gemini).

    The chain returns validated content; this function adds the
    metadata fields (course_id, created_at, total_days, etc.)
    that the rest of the application expects.
    """
    chain = _get_course_chain()

    # Chain returns: {title, description, learning_objectives, prerequisites,
    #                 weeks, assignments, flashcards}
    course_content = chain.generate(
        topic=topic,
        duration=duration,
        difficulty=difficulty,
        language=language,
    )

    # ── Add metadata fields that the app expects ────────────
    seed_input = f"{topic.lower()}_{duration}_{difficulty.lower()}_{language.lower()}"
    seed_hash = hashlib.md5(seed_input.encode()).hexdigest()

    course_content["course_id"] = f"course_{seed_hash[:12]}"
    course_content["difficulty"] = difficulty
    course_content["language"] = language
    course_content["duration_weeks"] = duration
    course_content["created_at"] = datetime.now()
    course_content["total_days"] = duration * 5

    logger.info(
        f"AI course generated successfully: '{course_content.get('title')}'"
    )
    return course_content


# ═══════════════════════════════════════════════════════════════
# MOCK FALLBACK PATH (original deterministic generator)
# ═══════════════════════════════════════════════════════════════

def _mock_course_generator(
    topic: str,
    duration: int = 4,
    difficulty: str = "beginner",
    language: str = "english"
) -> Dict[str, Any]:
    """
    Deterministic mock generator — produces identical output for
    identical inputs.  Used as fallback when AI is unavailable.
    """
    # Create deterministic seed based on inputs
    seed_input = f"{topic.lower()}_{duration}_{difficulty.lower()}_{language.lower()}"
    seed_hash = hashlib.md5(seed_input.encode()).hexdigest()

    # Convert hash to numeric seed for pseudo-random generation
    numeric_seed = int(seed_hash[:8], 16)

    # Generate course structure
    course_title = _generate_course_title(topic, difficulty, language)
    course_description = _generate_course_description(topic, difficulty, language)

    # Generate learning objectives
    objectives = _generate_learning_objectives(topic, difficulty, numeric_seed)

    # Generate prerequisites
    prerequisites = _generate_prerequisites(topic, difficulty, numeric_seed)

    # Generate weeks and days
    weeks = []
    for week_num in range(1, duration + 1):
        week = _generate_week(week_num, topic, difficulty, language, numeric_seed + week_num)
        weeks.append(week)

    # Generate assignments
    assignments = _generate_assignments(topic, difficulty, duration, numeric_seed)

    # Generate flashcards
    flashcards = _generate_flashcards(topic, difficulty, duration, numeric_seed)

    # Generate unique course ID
    course_id = f"course_{seed_hash[:12]}"

    course_data = {
        "course_id": course_id,
        "title": course_title,
        "description": course_description,
        "difficulty": difficulty,
        "language": language,
        "duration_weeks": duration,
        "learning_objectives": objectives,
        "prerequisites": prerequisites,
        "weeks": [week.dict() for week in weeks],
        "assignments": [assignment.dict() for assignment in assignments],
        "flashcards": [flashcard.dict() for flashcard in flashcards],
        "created_at": datetime.now(),
        "total_days": duration * 5  # Assume 5 days per week
    }

    return course_data


def mock_llm_rag_answer(query: str, context: str, course_title: str) -> str:
    """
    Mock LLM service that generates answers using RAG.

    Args:
        query: User's question
        context: Retrieved context chunks
        course_title: Course title for context

    Returns:
        Generated answer
    """
    query_lower = query.lower()
    context_lower = context.lower()

    # Simple keyword-based response generation
    if any(word in query_lower for word in ['what', 'define', 'explain']):
        if 'python' in context_lower:
            return ("Python is a high-level, interpreted programming language known for its "
                   "simple syntax and readability. In this course, you'll learn Python fundamentals "
                   "including variables, data types, control structures, functions, and object-oriented programming.")
        elif 'web' in context_lower:
            return ("Web development involves creating websites and web applications. "
                   "This course covers HTML, CSS, and JavaScript - the core technologies for "
                   "building modern web applications.")
        else:
            return f"Based on the course material, here's an explanation of your query about '{query}'. The course covers this topic in the relevant sections."

    elif any(word in query_lower for word in ['how', 'steps', 'process']):
        if 'install' in query_lower:
            return ("To install Python, visit python.org and download the latest version. "
                   "Run the installer and make sure to check 'Add Python to PATH'. "
                   "Verify installation by running 'python --version' in your command line.")
        elif 'create' in query_lower:
            return ("To create a new project, first set up your development environment. "
                   "Create a new directory, initialize it as a Git repository if needed, "
                   "and set up your preferred code editor with necessary extensions.")
        else:
            return f"Here are the steps to accomplish '{query}' based on the course content."

    elif any(word in query_lower for word in ['when', 'time', 'schedule']):
        return ("The course is structured over {} weeks with approximately 5 days of content per week. "
               "Each day typically requires 1-2 hours of study time. You can progress at your own pace "
               "based on your schedule.".format(_extract_weeks_from_context(context)))

    elif any(word in query_lower for word in ['why', 'reason', 'purpose']):
        if 'python' in context_lower:
            return ("Python is widely used because of its simplicity, readability, and versatility. "
                   "It's excellent for beginners due to its clean syntax and has extensive libraries "
                   "for web development, data science, AI, and automation.")
        else:
            return f"The reason for '{query}' is explained in the course materials. " \
                   "Check the relevant week/day sections for detailed explanations."

    elif any(word in query_lower for word in ['example', 'sample', 'demo']):
        if 'code' in query_lower:
            return ("Here's a simple example:\n\n```python\n# This is a basic Python example\nprint('Hello, World!')\n"
                   "name = input('What is your name? ')\nprint(f'Hello, {name}!')\n```\n\n"
                   "This demonstrates basic Python syntax including printing and user input.")
        else:
            return f"Examples for '{query}' can be found in the practical exercises section of the course."

    else:
        # Default response for other queries
        return (f"Great question about '{query}'! Based on the {course_title} course content, "
               "the answer can be found in the relevant sections. The course provides comprehensive "
               "coverage of this topic with practical examples and exercises.")


def _generate_course_title(topic: str, difficulty: str, language: str) -> str:
    """Generate course title"""
    base_title = topic.strip().title()
    if difficulty == "beginner":
        return f"Introduction to {base_title}: A Beginner's Guide"
    elif difficulty == "intermediate":
        return f"Mastering {base_title}: Intermediate Concepts"
    else:
        return f"Advanced {base_title}: Expert Level Training"


def _generate_course_description(topic: str, difficulty: str, language: str) -> str:
    """Generate course description"""
    if difficulty == "beginner":
        return (f"This comprehensive course provides a solid foundation in {topic}. "
               "Perfect for beginners with no prior experience, you'll learn fundamental concepts, "
               "practical skills, and build confidence through hands-on exercises.")
    elif difficulty == "intermediate":
        return (f"Take your {topic} skills to the next level with this intermediate course. "
               "Build upon basic knowledge and dive deeper into advanced concepts and techniques.")
    else:
        return (f"Master advanced {topic} concepts and techniques in this expert-level course. "
               "Designed for experienced practitioners looking to expand their expertise.")


def _generate_learning_objectives(topic: str, difficulty: str, seed: int) -> List[str]:
    """Generate learning objectives"""
    base_objectives = [
        f"Understand fundamental concepts of {topic}",
        f"Apply {topic} principles to solve real-world problems",
        f"Develop practical skills through hands-on exercises",
        f"Build a portfolio project demonstrating proficiency"
    ]

    if difficulty == "intermediate":
        base_objectives.extend([
            f"Analyze complex {topic} scenarios",
            f"Optimize solutions for performance and scalability",
            f"Implement advanced {topic} techniques"
        ])
    elif difficulty == "advanced":
        base_objectives.extend([
            f"Design enterprise-level {topic} solutions",
            f"Lead {topic} development teams and projects",
            f"Innovate with cutting-edge {topic} methodologies"
        ])

    # Use seed to shuffle and select objectives
    import random
    random.seed(seed)
    random.shuffle(base_objectives)
    return base_objectives[:min(4 + (["beginner", "intermediate", "advanced"].index(difficulty) * 2), len(base_objectives))]


def _generate_prerequisites(topic: str, difficulty: str, seed: int) -> List[str]:
    """Generate prerequisites"""
    if difficulty == "beginner":
        return ["Basic computer literacy", "No prior programming experience required"]
    elif difficulty == "intermediate":
        return ["Completion of beginner-level course", "Basic understanding of programming concepts"]
    else:
        return ["Strong foundation in intermediate concepts", "Experience with basic implementation"]


def _generate_week(week_num: int, topic: str, difficulty: str, language: str, seed: int) -> Week:
    """Generate a week structure"""
    import random
    random.seed(seed)

    week_titles = {
        "python": ["Python Basics", "Data Structures", "Control Flow", "Functions", "Object-Oriented Programming", "Error Handling", "File Operations", "Modules and Libraries"],
        "web development": ["HTML Fundamentals", "CSS Styling", "JavaScript Basics", "DOM Manipulation", "Responsive Design", "APIs and Fetch", "Frameworks Overview", "Project Development"],
        "machine learning": ["Statistics Foundation", "Python for ML", "Data Preprocessing", "Supervised Learning", "Unsupervised Learning", "Model Evaluation", "Deep Learning Basics", "ML Project Lifecycle"]
    }

    topic_lower = topic.lower()
    if topic_lower in week_titles:
        title = week_titles[topic_lower][week_num % len(week_titles[topic_lower])]
    else:
        title = f"Week {week_num}: Core Concepts"

    # Generate objectives
    objectives = [f"Learn {topic} concept {i+1} for week {week_num}" for i in range(3)]

    # Generate days
    days = []
    for day_num in range(1, 6):  # 5 days per week
        day = _generate_day(day_num, topic, difficulty, language, seed + day_num)
        days.append(day)

    return Week(
        week_number=week_num,
        title=title,
        objectives=objectives,
        days=days
    )


def _generate_day(day_num: int, topic: str, difficulty: str, language: str, seed: int) -> Day:
    """Generate a day structure"""
    import random
    random.seed(seed)

    day_titles = {
        "python": ["Variables and Data Types", "Operators and Expressions", "Input and Output", "String Manipulation", "List Operations"],
        "web development": ["HTML Structure", "CSS Selectors", "JavaScript Variables", "Functions and Events", "CSS Layout"],
        "machine learning": ["Descriptive Statistics", "Python Basics", "Data Cleaning", "Regression Analysis", "Classification Basics"]
    }

    topic_lower = topic.lower()
    if topic_lower in day_titles:
        title = day_titles[topic_lower][day_num % len(day_titles[topic_lower])]
    else:
        title = f"Day {day_num}: {topic} Fundamentals"

    # Generate content
    content = f"""## {title}

This section covers the essential concepts of {title.lower()} in {topic}.

**Key Topics:**
- Introduction to {title.lower()}
- Core principles and terminology
- Practical applications
- Common patterns and best practices

**Learning Activities:**
1. Read the theoretical concepts
2. Complete the hands-on exercises
3. Review the examples provided
4. Test your understanding with practice problems
"""

    # Generate objectives
    objectives = [f"Understand {title.lower()} concepts", f"Apply {title.lower()} in practice", f"Solve related problems"]

    # Generate activities
    activities = [
        f"Complete exercises for {title}",
        f"Read additional resources on {title}",
        f"Participate in discussion forums",
        f"Practice coding challenges"
    ]

    return Day(
        day_number=day_num,
        title=title,
        objectives=objectives,
        content=content,
        activities=activities
    )


def _generate_assignments(topic: str, difficulty: str, duration: int, seed: int) -> List[Assignment]:
    """Generate assignments"""
    import random
    random.seed(seed)

    assignments = []

    # Generate quiz assignment
    quiz_questions = [
        f"What is the fundamental concept of {topic}?",
        f"Which of the following is a key principle in {topic}?",
        f"How do you apply {topic} in real-world scenarios?"
    ]

    assignments.append(Assignment(
        title=f"{topic} Quiz - Week {duration//2}",
        type="MCQ",
        difficulty=difficulty,
        questions=quiz_questions,
        solutions=["Answer 1", "Answer 2", "Answer 3"]
    ))

    # Generate coding assignment if appropriate
    if any(word in topic.lower() for word in ['python', 'programming', 'code', 'development']):
        coding_questions = [
            f"Write a basic program that demonstrates {topic} concepts",
            f"Create a function that solves a common {topic} problem",
            f"Implement a class that shows object-oriented principles"
        ]
        assignments.append(Assignment(
            title=f"{topic} Coding Assignment",
            type="coding",
            difficulty=difficulty,
            questions=coding_questions,
            solutions=["Solution 1", "Solution 2", "Solution 3"]
        ))

    return assignments


def _generate_flashcards(topic: str, difficulty: str, duration: int, seed: int) -> List[Flashcard]:
    """Generate flashcards"""
    import random
    random.seed(seed)

    flashcards = []

    # Generate basic concept flashcards
    concepts = [f"{topic} Basics", "Key Terms", "Important Formulas", "Best Practices"]
    definitions = ["Fundamental understanding", "Essential vocabulary", "Mathematical relationships", "Industry standards"]

    for i, concept in enumerate(concepts):
        flashcards.append(Flashcard(
            front=concept,
            back=definitions[i % len(definitions)],
            category="Concept"
        ))

    return flashcards


def _extract_weeks_from_context(context: str) -> int:
    """Extract number of weeks from context"""
    # Simple heuristic to extract duration
    if "4 weeks" in context:
        return 4
    elif "6 weeks" in context:
        return 6
    elif "8 weeks" in context:
        return 8
    else:
        return 4  # Default