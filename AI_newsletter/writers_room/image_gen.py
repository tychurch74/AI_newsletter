import requests
import os
import openai
import cloudinary.uploader

from urllib.parse import urlparse
import cloudinary

with open("credentials.txt", "r") as file:
    cdn_cred = [line.strip() for line in file]

cloud_name = cdn_cred[0]
api_key = cdn_cred[1]
api_secret = cdn_cred[2]

cloudinary.config(cloud_name, api_key, api_secret)

openai_api_key = os.environ["OPENAI_API_KEY"]

img_style = "vaporwave"

prompt_messages = [
    {
        "role": "system",
        "content": f"Writer is a large language model trained by OpenAI that writes prompt-based image descriptions in the style of {img_style} in order to generate random images for a newsletter about artificial intelligence, machine learning and general computing. Make sure your response is under 375 characters in length. Your response should only include the generated image description and not contain any additional content or context. Your generated image description will be fed directly to a text to image generator (OpenAI's Dall-e 2).",
    }
]


def img_prompt_writer(img_style):
    openai.api_key = openai_api_key
    text = f"Create a detailed image prompt to generate a random image in the style of {img_style} to be used in a newsletter about artificial intelligence, machine learning, and general computing. The image prompt should be under 375 characters in length."
    prompt_messages.append({"role": "user", "content": text})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=prompt_messages
    )
    prompt_content = completion.choices[0].message.content
    return prompt_content


def image_generator(prompt, n=1, size="256x256"):
    openai.api_key = openai_api_key
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size,
    )
    img_url = response["data"][0]["url"]
    return img_url


def download_image(url):
    response = requests.get(url)

    if response.status_code == 200:
        filename = "cdn_sample.png"

        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Image saved as {filename}")
        return filename
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


def upload_image_to_cdn(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result["url"]


def image_html_gen():
    prompt = img_prompt_writer(img_style)
    url = image_generator(prompt)
    file_name = download_image(url)
    cdn_url = upload_image_to_cdn(file_name)
    return cdn_url
