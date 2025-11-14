from src.agents.type_classifier_agent import TypeClassifierAgent
import json

if __name__ == "__main__":
    agent = TypeClassifierAgent(project_id="sab-dev-nghp-jobs-4063")

    sample_case = {
        "id": "C1001",
        "name": "Login",
        "description": "Process to login",
        "customer": "ACME",
        "emails": "User reported issue via email",
        "priority": "Medium"
    }

    output = agent.classify(sample_case)
    print("Predicted Case Type:", output)