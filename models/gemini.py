import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiModel:
    _client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )
    _model = "models/gemini-flash-lite-latest"
    @classmethod
    def generate(cls, prompt: str) -> str:
        """
        Sends a prompt to Gemini and returns the response text.
        Retries automatically if Gemini is temporarily unavailable.
        """

        retries = 3

        for attempt in range(retries):
            try:
                response = cls._client.models.generate_content(
                    model=cls._model,
                    contents=prompt,
                )
                return response.text.strip()

            except Exception as e:
                print(f"\nGemini Error: {e}")

                if attempt < retries - 1:
                    print("Retrying in 20 seconds...\n")
                    time.sleep(20)
                else:
                    raise