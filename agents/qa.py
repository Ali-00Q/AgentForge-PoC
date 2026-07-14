import json
from pathlib import Path

from models.gemini import GeminiModel


class QAAgent:
    def __init__(self):
        prompt_path = Path("prompts/qa_prompt.txt")
        self.prompt_template = prompt_path.read_text(encoding="utf-8")

    def run(
        self,
        frontend_output: dict,
        backend_output: dict
    ) -> dict:
        """
        Performs a QA review of the frontend and backend implementations.

        The QA Agent identifies errors and bugs in the frontend and backend implementations

        It returns a structured QA report for the orchestrator, which sends the issues to the appropriate development agent.

        Args:
            frontend_output: Output produced by the Frontend Agent.
            backend_output: Output produced by the Backend Agent.

        Returns:
            Parsed JSON QA report.
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
                f"QA Agent returned invalid JSON.\n\n{response}"
            ) from e