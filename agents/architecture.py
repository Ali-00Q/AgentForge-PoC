import json
from pathlib import Path

from models.gemini import GeminiModel


class ArchitectureAgent:
    def __init__(self):
        prompt_path = Path("prompts/architecture_prompt.txt")
        self.prompt_template = prompt_path.read_text(encoding="utf-8")

    def run(self, requirements: dict, feedback: str | None = None) -> dict:
        """
        Generates or revises the software architecture.

        Args:
            requirements: Approved project requirements from the requirements agent.
            feedback: Optional feedback if the architecture was rejected.

        Returns:
            Parsed JSON response from Gemini.
        """

        prompt = self.prompt_template

        prompt = prompt.replace(
            "{{REQUIREMENTS}}",
            # because we want to pass the requirements as a JSON string, we need to convert it to a string first, indent 2 is to make the JSON string more readable, same for all the upcoming agents
            json.dumps(requirements, indent=2)
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
                f"Architecture Agent returned invalid JSON.\n\n{response}"
            ) from e