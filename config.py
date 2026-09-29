import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

    # You can change this in .env if needed.
    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash"
    )

    # Optional local LaMini model
    local_explainer_enabled: bool = (
        os.getenv("LOCAL_EXPLAINER_ENABLED", "false").lower() == "true"
    )

    local_explainer_model: str = os.getenv(
        "LOCAL_EXPLAINER_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    max_output_tokens: int = int(
        os.getenv("MAX_OUTPUT_TOKENS", "1024")
    )

    temperature: float = float(
        os.getenv("TEMPERATURE", "0.3")
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()