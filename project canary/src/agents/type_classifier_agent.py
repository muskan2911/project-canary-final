from google.cloud import aiplatform
from utils.prompts import TYPE_CLASSIFICATION_PROMPT
from vertexai.preview.generative_models import GenerativeModel
import vertexai

class TypeClassifierAgent:
    def __init__(self, project_id: str, location="us-central1"):
        aiplatform.init(project=project_id, location=location)
        model = GenerativeModel("gemini-2.0-flash")
        self.model = model


    def classify(self, case):
        prompt = TYPE_CLASSIFICATION_PROMPT.format(
            cases=case,
        )

        result = self.model.generate_content(prompt)
        return result.text.replace("```json", "").replace("```", "").strip().lower()
