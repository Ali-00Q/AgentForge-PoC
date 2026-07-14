from pathlib import Path
import json


def load_prompt(prompt_name: str, **kwargs) -> str:
    """
    Loads a prompt template and replaces placeholders.

    Example:
        load_prompt(
            "frontend_prompt",
            REQUIREMENTS=requirements,
            ARCHITECTURE=architecture,
            FEEDBACK="..."
        )
    """

    path = Path("prompts") / f"{prompt_name}.txt"

    prompt = path.read_text(encoding="utf-8")

    for key, value in kwargs.items():

        if isinstance(value, dict):
            value = json.dumps(value, indent=2)

        elif value is None:
            value = "None"

        prompt = prompt.replace(
            f"{{{{{key}}}}}",
            str(value)
        )
    return prompt