import json
import os
from pathlib import Path
from base64 import b64decode
import openai

PROMPT = "An eco-friendly computer from the 90s in the style of vaporwave"
DATA_DIR = Path.cwd() / "responses"

DATA_DIR.mkdir(exist_ok=True)

openai.api_key = os.getenv("OPENAI_API_KEY")


def image_generator(prompt, n=1, size="256x256", response_format="json"):
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size,
        response_format=response_format,
    )
    response = image_generator(PROMPT, n=10)

    file_name = DATA_DIR / f"{PROMPT[:5]}-{response['created']}.json"

    with open(file_name, mode="w", encoding="utf-8") as file:
        json.dump(response, file)
        return response


file_name = "An ec-1683070917.json"
DATA_DIR = Path.cwd() / "responses"
JSON_FILE = DATA_DIR / file_name
IMAGE_DIR = Path.cwd() / "images" / JSON_FILE.stem

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

with open(JSON_FILE, mode="r", encoding="utf-8") as file:
    response = json.load(file)

for index, image_dict in enumerate(response["data"]):
    image_data = b64decode(image_dict["b64_json"])
    image_file = IMAGE_DIR / f"{JSON_FILE.stem}-{index}.png"
    with open(image_file, mode="wb") as png:
        png.write(image_data)
