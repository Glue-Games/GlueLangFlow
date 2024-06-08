from benchmark.settings.modelsConfig import OPENAI_PROMPT_MODEL_THEME
from benchmark.models.baseModels.openaiBase import openai_base_model
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class OpenAIPromptModel:
    def __init__(self, client) -> None:
        self.model = "gpt-4-0125-preview"
        self.client = client.client

    def generate_image_prompt(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        messages.insert(0, OPENAI_PROMPT_MODEL_THEME)

        chat = self.client.chat.completions.create(model=self.model, messages=messages)
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply
    
    def __str__(self) -> str:
        return __class__.__name__

openai_prompt_model = OpenAIPromptModel(client=openai_base_model)