from benchmark.settings.modelsConfig import OPENAI_API_KEY
from openai import OpenAI

class OpenAIBaseModel:
    def __init__(self, client) -> None:
        self.client = client

openai_base_model = OpenAIBaseModel(OpenAI(api_key=OPENAI_API_KEY))