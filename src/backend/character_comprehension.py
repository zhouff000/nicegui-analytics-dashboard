from openai import OpenAI
import os
import dotenv
import tomllib

dotenv.load_dotenv("./.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _prompt_template(character, scenario):
    with open("src/backend/config/prompt.toml", "rb") as f:
        config = tomllib.load(f)["character_comprehension"]

    return config[scenario].format(character=character)



if __name__ == "__main__":
    print(_prompt_template("林", "pronunciation"))
    ...