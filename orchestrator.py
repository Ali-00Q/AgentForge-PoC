from human_approval import human_approval

from agents.requirements import RequirementsAgent
from agents.architecture import ArchitectureAgent
from agents.frontend import FrontendAgent
from agents.backend import BackendAgent
from agents.integration import IntegrationAgent
from agents.qa import QAAgent

class Orchestrator:

    def __init__(self):

        self.requirements_agent = RequirementsAgent()
        self.architecture_agent = ArchitectureAgent()
        self.frontend_agent = FrontendAgent()
        self.backend_agent = BackendAgent()
        self.integration_agent = IntegrationAgent()
        self.qa_agent = QAAgent()

    def run(self, project_brief):

        print("\n========== AgentForge ==========\n")

        # Requirements
        feedback = None

        while True:

            requirements = self.requirements_agent.run(
                project_brief,
                feedback
            )

            approved, feedback = human_approval(
                "Requirements",
                requirements
            )

            if approved:
                break

        # Architecture
        feedback = None

        while True:

            architecture = self.architecture_agent.run(
                requirements,
                feedback
            )

            approved, feedback = human_approval(
                "Architecture",
                architecture
            )

            if approved:
                break


        # Generating frontend and backend
        print("\nGenerating frontend...\n")

        frontend = self.frontend_agent.run(
            requirements,
            architecture
        )

        print("\nGenerating backend...\n")

        backend = self.backend_agent.run(
            requirements,
            architecture
        )

        # Integration Loop
        while True:

            integration = self.integration_agent.run(
                frontend,
                backend
            )

            if integration["passed"]:
                print("\nIntegration Passed.\n")
                break

            print("\nIntegration Failed.\n")

            for issue in integration["issues"]:
                print(
                    f'{issue["agent"]}: {issue["description"]}'
                )

                if issue["agent"] == "frontend":
                    frontend = self.frontend_agent.run(
                        requirements,
                        architecture,
                        feedback=issue["description"]
                    )

                elif issue["agent"] == "backend":
                    backend = self.backend_agent.run(
                        requirements,
                        architecture,
                        feedback=issue["description"]
                    )

        # QA Loop
        while True:

            qa = self.qa_agent.run(
                frontend,
                backend
            )

            if qa["passed"]:
                print("\nQA Passed.\n")
                break

            print("\nQA Failed.\n")

            for issue in qa["issues"]:
                print(
                    f'{issue["agent"]}: {issue["description"]}'
                )

                if issue["agent"] == "frontend":
                    frontend = self.frontend_agent.run(
                        requirements,
                        architecture,
                        feedback=issue["description"]
                    )

                elif issue["agent"] == "backend":
                    backend = self.backend_agent.run(
                        requirements,
                        architecture,
                        feedback=issue["description"]
                    )

        # Final approval
        human_approval(
            "Final Review",
            "The project has passed Integration and QA."
        )

        print("\nWorkflow Complete.\n")