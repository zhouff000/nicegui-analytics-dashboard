from openai import OpenAI
import os
import dotenv
import tomllib

# ...existing code...
from pathlib import Path
from functools import lru_cache

dotenv.load_dotenv(dotenv.find_dotenv(), override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROJECT_CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"
PROMPT_TOML_PATH = Path(
    os.getenv("PROMPT_TOML_PATH", PROJECT_CONFIG_DIR / "prompt.toml")
)
CC_CONFIG_TOML_PATH = Path(
    os.getenv("CC_CONFIG_TOML_PATH", PROJECT_CONFIG_DIR / "config.toml")
)


@lru_cache(maxsize=1)
def _load_prompts():
    with open(PROMPT_TOML_PATH, "rb") as f:
        return tomllib.load(f)["character_comprehension"]


@lru_cache(maxsize=1)
def _load_cc_config():
    with open(CC_CONFIG_TOML_PATH, "rb") as f:
        return tomllib.load(f)["character_comprehension"]


def _prompt_template(character, scenario):
    prompt = _load_prompts()
    return prompt[scenario].format(character=character)


def chat_response(character, scenario, stream=False):
    config = _load_cc_config()
    message = _prompt_template(character, scenario)
    response = client.chat.completions.create(
        model=config[scenario]["openai_model"],
        messages=[{"role": "user", "content": message}],
        stream=stream,
    )
    return response


if __name__ == "__main__":
    for chunk in chat_response("林", "practice", stream=True):
        if chunk.choices[0].delta.reasoning_content:
            print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
        else:
            print(chunk.choices[0].delta.content, end="", flush=True)
    ...
