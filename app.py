from orchestrator import Orchestrator

print("AgentForge Proof of Concept")

brief = input("\nDescribe your application:\n\n")

orchestrator = Orchestrator()

orchestrator.run(brief)