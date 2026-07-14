import json
from pathlib import Path

from models.gemini import GeminiModel


class IntegrationAgent:
    def __init__(self):
        prompt_path = Path("prompts/integration_prompt.txt")
        self.prompt_template = prompt_path.read_text(encoding="utf-8")

    def run(
        self,
        frontend_output: dict,
        backend_output: dict
    ) -> dict:
        """
        Only validates whether the frontend and backend apis are compatible, for now

        Args:
            frontend_output: Output from the Frontend Agent.
            backend_output: Output from the Backend Agent.

        Returns:
            Parsed JSON response from Gemini.
        """

        prompt = self.prompt_template

        prompt = prompt.replace(
            "{{FRONTEND_OUTPUT}}",
            json.dumps(frontend_output, indent=2)
        )

        prompt = prompt.replace(
            "{{BACKEND_OUTPUT}}",
            json.dumps(backend_output, indent=2)
        )

        response = GeminiModel.generate(prompt)

        try:
            return json.loads(response)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Integration Agent returned invalid JSON.\n\n{response}"
            ) from e