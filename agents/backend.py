import json
from pathlib import Path

from models.gemini import GeminiModel


class BackendAgent:
    def __init__(self):
        prompt_path = Path("prompts/backend_prompt.txt")
        self.prompt_template = prompt_path.read_text(encoding="utf-8")

    def run(
        self,
        requirements: dict,
        architecture: dict,
        feedback: str | None = None
    ) -> dict:
        """
        Generates or revises the backend implementation.

        Args:
            requirements: Approved project requirements.
            architecture: Approved software architecture.
            feedback: Optional feedback from Integration or QA.

        Returns:
            Parsed JSON response from Gemini.
        """

        prompt = self.prompt_template

        prompt = prompt.replace(
            "{{REQUIREMENTS}}",
            json.dumps(requirements, indent=2)
        )

        prompt = prompt.replace(
            "{{ARCHITECTURE}}",
            json.dumps(architecture, indent=2)
        )

        prompt = prompt.replace(
            "{{FEEDBACK}}",
            feedback.strip() if feedback else "None"
        )

        response = GeminiModel.generate(prompt)

        try:
            return json.loads(response)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Backend Agent returned invalid JSON.\n\n{response}"
            ) from e