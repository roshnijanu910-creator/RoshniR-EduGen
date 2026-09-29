from gemini_client import generate_text


def summarize_text(text: str) -> str:

    prompt = (
        "Summarize the following educational passage "
        "while preserving its important facts, definitions, "
        "relationships, and conclusions.\n\n"
        "PASSAGE:\n"
        + text
    )

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie, a study assistant. "
            "Create a concise and easy-to-revise summary. "
            "Remove repetition but do not remove important information. "
            "Use simple English."
        ),
    )