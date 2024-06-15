from serverAILibrary.models.promptModels.openaiPromptModel import openai_prompt_model
from serverAILibrary.models.imageModels.openaiImageModel import openai_image_model
from serverAILibrary.models.backgroundModels.openaiBackgroundModel import openai_background_model
from serverAILibrary.imagePostProcess import get_shrinked_image
import requests
from io import BytesIO

class AIInterface:
    def __init__(self, context) -> None:

        # TODO: add default/empty values
        self.context = context
        
        self.prompt_context = context['context-2']
        self.full_level_context = context['inputs-5']

        # TODO: change to input from pipelien
        self.level_caption_inputs = context['inputs-1'].split(",")[0]

    def step_caption_to_image_prompt(self, level_caption_inputs):
        return level_caption_inputs, openai_prompt_model.generate_image_prompt(level_caption_inputs, context=self.prompt_context)

    def step_image_from_prompt(self, image_prompt):
        url = openai_image_model.generate_image(image_prompt)
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        image_data = BytesIO(response.content)
        return url, image_data
    
    def step_picture_to_full_level(self, processed_image):
        return openai_background_model.fill_background_image(processed_image, context=self.full_level_context)

    def run_pipeline(self):
        # step 0 - user agent/ trend not implemented currently
        yield "not implemented"

        # step 1 - generate level caption from trend/user agent not implemented currently
        yield "not implemented"
        
        # step 2 - caption to prompt
        _, image_prompt = self.step_caption_to_image_prompt(self.level_caption_inputs)
        yield image_prompt

        # step 3 - image from prompt
        url, image = self.step_image_from_prompt(image_prompt)
        yield url

        # step 4 - process image to remove background
        processed_image = get_shrinked_image(image)
        yield processed_image

        # step 5 - process image and background generation
        full_level_url = self.step_picture_to_full_level(processed_image)
        yield full_level_url
