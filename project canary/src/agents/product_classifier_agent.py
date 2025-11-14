from google.cloud import aiplatform
from src.utils.prompts import PRODUCT_CLASSIFICATION_PROMPT
from vertexai.preview.generative_models import GenerativeModel
import vertexai

class ProductClassifierAgent:

    def __init__(self, project_id: str, location="us-central1"):
        aiplatform.init(project=project_id, location=location)
        model = GenerativeModel("gemini-2.0-flash")
        self.model = model

    def classify(self, case):
        prompt = PRODUCT_CLASSIFICATION_PROMPT.format(
            case_id=case["id"],
            case_name=case["name"],
            case_description=case["description"],
            case_customer_info=case["customer"],
            case_emails=case["emails"],
            customer_priority=case["priority"],
        )

        response = self.model.generate_content(prompt)
        return response.text.strip().lower()