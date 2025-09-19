from openai import OpenAI
import os
import dotenv
import tomllib
from typing import Dict, Any, Optional, Union, Generator
from pathlib import Path
from functools import lru_cache
from ..database.sqlite import DatabaseManager

__all__ = [
    "generate_character_response",
    "get_character_from_database",
    "get_character_response",
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


@lru_cache(maxsize=1)
def _load_prompt_templates() -> Dict[str, Any]:
    """Load prompt templates from TOML configuration."""
    try:
        with open(_PROMPT_CONFIG_PATH, "rb") as f:
            return tomllib.load(f)["character_comprehension"]
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


def _build_prompt_message(character: str, scenario: str) -> str:
    """Build prompt message for given character and scenario."""
    prompts = _load_prompt_templates()

    if scenario not in prompts:
        raise ValueError(f"Scenario '{scenario}' not found in prompt templates")

    return prompts[scenario].format(character=character)


def generate_character_response(
    character: str, scenario: str, stream: bool = False
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

    message = _build_prompt_message(character, scenario)

    try:
        return _openai_client.chat.completions.create(
            model=config[scenario]["openai_model"],
            messages=[{"role": "user", "content": message}],
            stream=stream,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to generate character response: {e}")


def get_character_from_database(character: str) -> Optional[Dict[str, Any]]:
    """Retrieve character data from database.

    Args:
        character: The character to search for

    Returns:
        Character data dict if found and complete, None otherwise
    """
    try:
        db = DatabaseManager()
        db.get_connection()
        character_data = db.execute_single(
            "SELECT * FROM documents WHERE Character = ?", (character,)
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
    character: str, scenario: str, stream: bool = False
) -> Union[Dict[str, Any], Any, Generator]:
    """Get character response from database or generate new one.

    First attempts to retrieve from database. If not found or incomplete,
    generates a new response using AI.

    Args:
        character: The character to analyze
        scenario: The scenario type
        stream: Whether to stream AI response if generation is needed

    Returns:
        Database result dict or AI response/generator
    """
    # Try database first
    db_result = get_character_from_database(character)
    if db_result is not None:
        return db_result

    # Generate new response if not in database
    return generate_character_response(character, scenario, stream)


# Maintain backward compatibility
chat_response = generate_character_response
database_result = get_character_from_database
response_and_db = get_character_response

if __name__ == "__main__":
    # Example usage
    try:
        response = get_character_response("林", "practice")
        print(f"Response type: {type(response)}")

        # Streaming example:
        # for chunk in generate_character_response("林", "practice", stream=True):
        #     if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
        #         print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
        #     elif hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
        #         print(chunk.choices[0].delta.content, end="", flush=True)

    except Exception as e:
        print(f"Error: {e}")
