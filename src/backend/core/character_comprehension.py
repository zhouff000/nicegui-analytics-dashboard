from openai import OpenAI
import os
import dotenv
import tomllib
from typing import Dict, Any, Optional, Union, Generator
from pathlib import Path
from functools import lru_cache
from ..database.sqlite import DatabaseManager
import re
from ..utils.paddle_ocr import call_ocr
from .dataclass import (
    CharacterResponse,
    create_database_response,
    create_llm_response,
)

__all__ = [
    "llm_character_response",
    "get_character_response",
    "CharacterResponse",
]

dotenv.load_dotenv(dotenv.find_dotenv(), override=True)

# Initialize OpenAI client
_openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuration paths
_PROJECT_CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"
_PROMPT_CONFIG_PATH = Path(
    os.getenv("PROMPT_TOML_PATH", _PROJECT_CONFIG_DIR / "prompt.toml")
)
_CHARACTER_CONFIG_PATH = Path(
    os.getenv("CC_CONFIG_TOML_PATH", _PROJECT_CONFIG_DIR / "config.toml")
)
_DB_FILE_PATH = Path(__file__).resolve().parents[3] / "sqlite3" / "main.db"


def _is_valid_image_path(path_str: str) -> bool:
    if not os.path.isfile(path_str):
        return False
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
    return Path(path_str).suffix.lower() in valid_extensions


def _extract_first_chinese_character(text: str) -> Optional[str]:
    if not text:
        return None

    chinese_pattern = r"[\u4e00-\u9fff]"
    match = re.search(chinese_pattern, text)
    return match.group() if match else None


def _extract_first_character(input_str: str) -> str:
    """Extract the first Chinese character from input

    Args:
        input_str: Input string, could be a single Chinese character or image path

    Returns:
        The first Chinese character extracted

    Raises:
        ValueError: If no valid Chinese character can be extracted
    """
    # Case 1: Direct single Chinese character
    if len(input_str) == 1 and "\u4e00" <= input_str <= "\u9fff":
        return input_str

    # Case 2: Image path, use OCR
    if _is_valid_image_path(input_str):
        try:
            ocr_text = call_ocr(file_path=input_str)
            first_char = _extract_first_chinese_character(ocr_text)
            if first_char:
                return first_char
            else:
                raise ValueError(
                    f"No Chinese character found in OCR result: {ocr_text}"
                )
        except Exception as e:
            raise ValueError(f"OCR processing failed: {e}")

    # Case 3: Text string containing Chinese characters
    first_char = _extract_first_chinese_character(input_str)
    if first_char:
        return first_char

    # If none match, raise exception
    raise ValueError(f"Unable to extract Chinese character from input: '{input_str}'")


@lru_cache(maxsize=1)
def _load_prompt_templates(locale) -> Dict[str, Any]:
    """Load prompt templates from TOML configuration."""
    try:
        with open(_PROMPT_CONFIG_PATH, "rb") as f:
            return tomllib.load(f)["character_comprehension"][locale]
    except (FileNotFoundError, KeyError, tomllib.TOMLDecodeError) as e:
        raise RuntimeError(f"Failed to load prompt templates: {e}")


@lru_cache(maxsize=1)
def _load_character_config() -> Dict[str, Any]:
    """Load character comprehension configuration from TOML file."""
    try:
        with open(_CHARACTER_CONFIG_PATH, "rb") as f:
            return tomllib.load(f)["character_comprehension"]
    except (FileNotFoundError, KeyError, tomllib.TOMLDecodeError) as e:
        raise RuntimeError(f"Failed to load character config: {e}")


def _build_prompt_message(character: str, scenario: str, locale: str) -> str:
    """Build prompt message for given character and scenario."""
    prompts = _load_prompt_templates(locale)

    if scenario not in prompts:
        raise ValueError(f"Scenario '{scenario}' not found in prompt templates")

    return prompts[scenario].format(character=character)


def llm_character_response(
    character: str, scenario: str, locale: str, stream: bool = False
) -> Union[Any, Generator]:
    """Generate AI response for character in given scenario.

    Args:
        character: The character to analyze
        scenario: The scenario type (e.g., 'practice')
        stream: Whether to stream the response

    Returns:
        OpenAI chat completion response or generator if streaming
    """
    config = _load_character_config()

    if scenario not in config:
        raise ValueError(f"Scenario '{scenario}' not found in configuration")

    message = _build_prompt_message(character, scenario, locale)

    try:
        return _openai_client.chat.completions.create(
            model=config[scenario]["openai_model"],
            messages=[{"role": "user", "content": message}],
            stream=stream,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to generate character response: {e}")


def database_character_response(
    character: str, locale: str
) -> Optional[Dict[str, Any]]:
    """Retrieve character data from database.

    Args:
        character: The character to search for

    Returns:
        Character data dict if found and complete, None otherwise
    """
    try:
        db = DatabaseManager(_DB_FILE_PATH)
        db.get_connection()
        character_data = db.execute_single(
            "SELECT * FROM character_comprehension WHERE character = ? AND locale = ?",
            (character, locale),
        )

        # Return None if data doesn't exist or has incomplete fields
        if not character_data or any(
            value is None for value in character_data.values()
        ):
            return None

        return character_data

    except Exception as e:
        # Log error in production, for now just return None
        print(f"Database error: {e}")
        return None


def get_character_response(
    input_str: str, scenario: str, stream: bool = False, locale: str = "en"
) -> CharacterResponse:
    """Get character response with unified format.

    First extracts the first Chinese character from input (direct character or OCR from image),
    then attempts to retrieve from database. If not found or incomplete,
    generates a new response using AI.

    Args:
        input_str: Input string (single Chinese character or image path)
        scenario: The scenario type
        stream: Whether to stream AI response if generation is needed

    Returns:
        CharacterResponse object with unified interface
    """
    # Extract the first Chinese character
    character = _extract_first_character(input_str)

    # Try database first
    db_result = database_character_response(character, locale)
    if db_result is not None:
        return create_database_response(character, scenario, db_result)

    # Generate new response if not in database
    llm_response = llm_character_response(
        character=character, scenario=scenario, stream=stream, locale=locale
    )
    return create_llm_response(
        character=character, scenario=scenario, llm_response=llm_response, stream=stream
    )
