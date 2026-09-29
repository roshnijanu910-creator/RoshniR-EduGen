from functools import lru_cache
import time

from google import genai
from google.genai import types

from config import get_settings


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini is not configured correctly."""


@lru_cache(maxsize=1)
def get_client():
    settings = get_settings()

    if not settings.gemini_api_key:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(
    prompt: str,
    system_instruction: str | None = None
) -> str:

    settings = get_settings()
    client = get_client()

    last_error = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.temperature,
                    max_output_tokens=settings.max_output_tokens,
                    system_instruction=system_instruction,
                ),
            )

            text = getattr(response, "text", None)

            if not text or not text.strip():
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except Exception as exc:
            last_error = exc

            if attempt < 2:
                time.sleep(2)

    raise RuntimeError(
        "Gemini is temporarily unavailable. "
        "Please click Generate again in a moment. "
        f"Details: {last_error}"
    )