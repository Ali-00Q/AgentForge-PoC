
import json
from pathlib import Path

from models.gemini import GeminiModel


class RequirementsAgent:
    def __init__(self):
        prompt_path = Path("prompts/requirements_prompt.txt")
        self.prompt_template = prompt_path.read_text(encoding="utf-8")

    def run(self, project_brief: str, feedback: str | None = None) -> dict:
        """
        Generates project requirements.

        Args:
            project_brief: User's original project description.
            feedback: Optional feedback if the previous requirements were rejected.

        Returns:
            Parsed JSON response from Gemini.
        """

        prompt = self.prompt_template

        prompt = prompt.replace(
            "{{PROJECT_BRIEF}}",
            project_brief.strip()
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
                f"Requirements Agent returned invalid JSON.\n\n{response}"
            ) from e