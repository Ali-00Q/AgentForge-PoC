import json
from models.gemini import GeminiModel


class IntegrationAgent:

    def run(self, prompt: str):

        response = GeminiModel.generate(prompt)
        return json.loads(response)