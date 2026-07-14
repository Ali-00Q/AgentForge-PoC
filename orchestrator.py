from human_approval import human_approval
from prompt_loader import load_prompt

from agents.requirements import RequirementsAgent
from agents.architecture import ArchitectureAgent
from agents.frontend import FrontendAgent
from agents.backend import BackendAgent
from agents.integration import IntegrationAgent
from agents.qa import QAAgent


MAX_RETRIES = 2


class Orchestrator:

    def __init__(self):

        self.requirements_agent = RequirementsAgent()
        self.architecture_agent = ArchitectureAgent()
        self.frontend_agent = FrontendAgent()
        self.backend_agent = BackendAgent()
        self.integration_agent = IntegrationAgent()
        self.qa_agent = QAAgent()

    def run(self, project_brief: str):

        print("\n========== AgentForge ==========\n")


        # Requirements
        feedback = None

        while True:

            prompt = load_prompt(
                "requirements_prompt",
                PROJECT_BRIEF=project_brief,
                FEEDBACK=feedback
            )

            requirements = self.requirements_agent.run(prompt)

            approved, feedback = human_approval(
                "Requirements",
                requirements
            )

            if approved:
                break

        print("\nRequirements Approved.\n")


        # Architecture
        feedback = None

        while True:

            prompt = load_prompt(
                "architecture_prompt",
                REQUIREMENTS=requirements,
                FEEDBACK=feedback
            )

            architecture = self.architecture_agent.run(prompt)

            approved, feedback = human_approval(
                "Architecture",
                architecture
            )

            if approved:
                break

        print("\nArchitecture Approved.\n")


        # Generating frontend and backend
        frontend_prompt = load_prompt(
            "frontend_prompt",
            REQUIREMENTS=requirements,
            ARCHITECTURE=architecture,
            FEEDBACK=None
        )

        backend_prompt = load_prompt(
            "backend_prompt",
            REQUIREMENTS=requirements,
            ARCHITECTURE=architecture,
            FEEDBACK=None
        )

        print("Generating frontend...")
        frontend = self.frontend_agent.run(frontend_prompt)

        print("Generating backend...")
        backend = self.backend_agent.run(backend_prompt)


        # Integration loop
        for attempt in range(MAX_RETRIES):

            integration_prompt = load_prompt(
                "integration_prompt",
                FRONTEND_OUTPUT=frontend,
                BACKEND_OUTPUT=backend
            )

            integration = self.integration_agent.run(integration_prompt)

            if integration.get("passed", False):

                print("\nIntegration Passed.\n")
                break

            print("\nIntegration Failed.\n")

            for issue in integration.get("issues", []):

                agent = issue["agent"].lower()
                description = issue["description"]

                print(f"[{agent}] {description}")

                if agent == "frontend":

                    frontend_prompt = load_prompt(
                        "frontend_prompt",
                        REQUIREMENTS=requirements,
                        ARCHITECTURE=architecture,
                        FEEDBACK=description
                    )

                    frontend = self.frontend_agent.run(frontend_prompt)

                elif agent == "backend":

                    backend_prompt = load_prompt(
                        "backend_prompt",
                        REQUIREMENTS=requirements,
                        ARCHITECTURE=architecture,
                        FEEDBACK=description
                    )

                    backend = self.backend_agent.run(backend_prompt)

        else:

            print("\nIntegration failed after maximum retries.")
            return


        # QA loop
        for attempt in range(MAX_RETRIES):

            qa_prompt = load_prompt(
                "qa_prompt",
                FRONTEND_OUTPUT=frontend,
                BACKEND_OUTPUT=backend
            )

            qa = self.qa_agent.run(qa_prompt)

            if qa.get("passed", False):

                print("\nQA Passed.\n")
                break

            print("\nQA Failed.\n")

            for issue in qa.get("issues", []):

                agent = issue["agent"].lower()
                description = issue["description"]

                print(f"[{agent}] {description}")

                if agent == "frontend":

                    frontend_prompt = load_prompt(
                        "frontend_prompt",
                        REQUIREMENTS=requirements,
                        ARCHITECTURE=architecture,
                        FEEDBACK=description
                    )

                    frontend = self.frontend_agent.run(frontend_prompt)

                elif agent == "backend":

                    backend_prompt = load_prompt(
                        "backend_prompt",
                        REQUIREMENTS=requirements,
                        ARCHITECTURE=architecture,
                        FEEDBACK=description
                    )

                    backend = self.backend_agent.run(backend_prompt)

        else:

            print("\nQA failed after maximum retries.")
            return


        # Human approval
        approved, _ = human_approval(
            "Final Review",
            {
                "requirements": requirements,
                "architecture": architecture,
                "frontend": frontend,
                "backend": backend
            }
        )

        if approved:
            print("\nProject Approved!\n")
        else:
            print("\nProject Rejected by Human.\n")

        return {
            "requirements": requirements,
            "architecture": architecture,
            "frontend": frontend,
            "backend": backend
        }