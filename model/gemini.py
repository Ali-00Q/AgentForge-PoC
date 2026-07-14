from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
class GeminiModel:
    _client = genai.Client(
        api_key = os.getenv("GEMINI_API_KEY")
    )
    _model = "gemini-2.5-flash"
    @classmethod
    def generate(cls, prompt: str) -> str:
        response = cls._client.models.generate_content(
            model=cls._model,
            contents=prompt,
        )
        return response.text.strip()
