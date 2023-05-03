import json
import os
from pathlib import Path
from base64 import b64decode
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")


def image_generator(prompt, n=1, size="256x256"):
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size,
    )
    img_url = response["data"][0]["url"]
    return img_url


prompt = "A picture of a messy desk with a 90s era computer on the desk in the style of vaporwave"
print(image_generator(prompt))
