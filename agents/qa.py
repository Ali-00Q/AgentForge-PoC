import json
from models.gemini import GeminiModel


class QAAgent:

    def run(self, prompt: str):

        response = GeminiModel.generate(prompt)
        return json.loads(response)