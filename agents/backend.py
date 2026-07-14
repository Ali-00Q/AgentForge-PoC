import json
from models.gemini import GeminiModel


class BackendAgent:

    def run(self, prompt: str):

        response = GeminiModel.generate(prompt)
        return json.loads(response)