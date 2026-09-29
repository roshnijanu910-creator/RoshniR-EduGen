from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:

    prompt = f"""
Create a personalized learning path for:

{topic}

Organize the learning path into:

1. Beginner Foundations
2. Intermediate Concepts
3. Advanced Concepts
4. Suggested Timeline
5. Practice Activities
6. Mini Projects
7. Recommended Resource Types

For every stage, explain what the learner should study.

Make the plan realistic for a student.

Do not create fake URLs.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie, an educational learning-plan designer. "
            "Create structured and achievable learning paths. "
            "Start from beginner level and gradually move to advanced level. "
            "Use clear headings and simple English."
        ),
    )