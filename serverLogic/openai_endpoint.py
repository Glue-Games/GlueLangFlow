from serverLogic.settings import API_KEY, CHAT_THEME
from openai import OpenAI

import urllib.request
import os
import logging
import uvicorn

logger = logging.getLogger("uvicorn")

client = OpenAI(api_key=API_KEY)

OPTION_MODELS = ["gpt-4-vision-preview", "dall-e-3"]

def get_create_image(prompt):
    response = client.images.generate(prompt=prompt,
    n=1,
    size="1024x1024",
    quality="standard",
    model= "dall-e-3")

    logger.info(response.data)
    logger.info(response.data[0])
    url = response.data[0].url
    return url
