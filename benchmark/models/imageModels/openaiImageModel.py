from benchmark.settings.modelsConfig import OPENAI_PROMPT_MODEL_THEME
from benchmark.models.baseModels.openaiBase import openai_base_model
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class OpenAIImageModel:
    def __init__(self, client) -> None:
        self.model = "dall-e-3"
        self.client = client.client

    def generate_image(self, prompt):
        response = self.client.images.generate(
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard",
            model=self.model
        )

        # logger.info(response.data)
        # logger.info(response.data[0])
        url = response.data[0].url
        return url

    def __str__(self) -> str:
        return __class__.__name__

openai_image_model = OpenAIImageModel(client=openai_base_model)