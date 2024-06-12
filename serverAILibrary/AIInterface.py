from serverAILibrary.models.promptModels.openaiPromptModel import openai_prompt_model
from serverAILibrary.models.imageModels.openaiImageModel import openai_image_model
from serverAILibrary.models.backgroundModels.openaiBackgroundModel import openai_background_model
from serverAILibrary.imagePostProcess import get_shrinked_image
import requests
from io import BytesIO

class AIInterface:
    def __init__(self, context) -> None:
        self.context = context
        self.prompt_context = context['Caption to Image Prompt']
        self.full_level_context = context['Background Generator']

        # TODO: change to input from pipelien
        self.level_caption = context['Level Caption Generator'].split(",")[0]

    def step_caption_to_image_prompt(self, level_caption):
        return level_caption, openai_prompt_model.generate_image_prompt(level_caption, context=self.prompt_context)

    def step_image_from_prompt(self, image_prompt):
        url = openai_image_model.generate_image(image_prompt)
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        image_data = BytesIO(response.content)
        return url, image_data
    
    def step_picture_to_full_level(self, image):
        img_bytes = get_shrinked_image(image)
        return openai_background_model.fill_background_image(img_bytes, context=self.full_level_context)

    def run_pipeline(self):
        _, image_prompt = self.step_caption_to_image_prompt(self.level_caption)
        yield image_prompt

        url, image = self.step_image_from_prompt(image_prompt)
        yield url

        full_level_url = self.step_picture_to_full_level(image)
        yield full_level_url
