import json
import re

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    """
    Removes Markdown code blocks and extracts
    the JSON array from Gemini's response.
    """

    text = text.strip()

    # Remove ```json
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove closing ```
    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    # Find JSON array
    start = text.find("[")
    end = text.rfind("]")

    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]

    return text.strip()


def validate_quiz(data, count: int):

    if not isinstance(data, list):

        raise ValueError(
            "Quiz response must be a JSON array."
        )

    if len(data) < count:

        raise ValueError(
            f"Expected {count} questions, "
            f"but received {len(data)}."
        )

    normalized = []

    for index, item in enumerate(
        data[:count],
        start=1
    ):

        if not isinstance(item, dict):

            raise ValueError(
                f"Question {index} is invalid."
            )

        question = str(
            item.get("question", "")
        ).strip()

        options = item.get("options")

        correct_answer = str(
            item.get("correct_answer", "")
        ).strip()

        explanation = str(
            item.get("explanation", "")
        ).strip()

        if not question:

            raise ValueError(
                f"Question {index} has no question."
            )

        if not isinstance(options, list):

            raise ValueError(
                f"Question {index} options are invalid."
            )

        if len(options) != 4:

            raise ValueError(
                f"Question {index} must have exactly 4 options."
            )

        options = [
            str(option).strip()
            for option in options
        ]

        if correct_answer not in options:

            raise ValueError(
                f"Question {index} has an invalid correct answer."
            )

        normalized.append(
            {
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation,
            }
        )

    return normalized


def generate_quiz(
    passage: str,
    count: int = 3
):

    prompt = f"""
Create exactly {count} multiple-choice questions
from the educational text below.

Each question must contain:

- One question
- Exactly four options
- One correct answer
- A short explanation

Return ONLY valid JSON.

Use exactly this format:

[
  {{
    "question": "Question here",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Option A",
    "explanation": "Short explanation."
  }}
]

Educational text:

{passage}
"""

    raw = generate_text(
        prompt,
        system_instruction=(
            "You are an educational MCQ generator. "
            "Create accurate questions from the supplied text. "
            "The response must contain ONLY valid JSON. "
            "Do not add Markdown or explanations outside the JSON."
        ),
    )

    try:

        cleaned = clean_json_block(raw)

        data = json.loads(cleaned)

        return validate_quiz(
            data,
            count
        )

    except (
        json.JSONDecodeError,
        ValueError,
        TypeError,
    ) as exc:

        raise RuntimeError(
            f"Quiz generation failed: {exc}"
        ) from exc