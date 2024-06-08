from benchmark.settings.modelsConfig import OPENAI_BACKGROUND_MODEL_PROMPT
from benchmark.models.baseModels.openaiBase import openai_base_model
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class OpenAIBackgroundModel:
    def __init__(self, client) -> None:
        self.model = "image-dalle-2"
        self.client = client.client
        self.prompt = OPENAI_BACKGROUND_MODEL_PROMPT

    def fill_background_image(self, img):
        # Make an API request to DALL-E 2 Edits
        response = self.client.images.edit(
            image=img,
            mask=img,
            prompt=self.prompt,
            n=1,
            size="1024x1024"
        )

        url = response.data[0].url
        return url

    def __str__(self) -> str:
        return __class__.__name__

openai_background_model = OpenAIBackgroundModel(client=openai_base_model)