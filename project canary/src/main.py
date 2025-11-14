from src.agents.type_classifier_agent import TypeClassifierAgent
from src.agents.product_classifier_agent import ProductClassifierAgent
import json

if __name__ == "__main__":
    TypeAgent = TypeClassifierAgent(project_id="sab-dev-nghp-jobs-4063")
    ProductAgent = ProductClassifierAgent(project_id="sab-dev-nghp-jobs-4063")

    sample_case = {
        "id": "C1001",
        "name": "Hilton Issue",
        "description": "Hilton Properties are not shoppable",
        "customer": "ACME",
        "emails": "User reported issue via email",
        "priority": "Medium"
    }

    type_agent_output = TypeAgent.classify(sample_case)
    product_agent_output = ProductAgent.classify(sample_case)

    print("Type:", type_agent_output)
    print("Product:", product_agent_output)