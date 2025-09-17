from openai import OpenAI
import os
import dotenv
import tomllib

dotenv.load_dotenv("./.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _prompt_template(character, scenario):
    with open("src/backend/config/prompt.toml", "rb") as f:
        prompt = tomllib.load(f)["character_comprehension"]

    return prompt[scenario].format(character=character)


def chat_response(character, scenario, stream=False):
    with open("src/backend/config/config.toml", "rb") as f:
        config = tomllib.load(f)["character_comprehension"]

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
