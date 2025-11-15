from google.cloud import aiplatform
from utils.prompts import SENTIMENT_CLASSIFICATION_PROMPT
from utils.prompts import CASE_TO_TRACKING_ID_PROMPT
from utils.prompts import CASE_ROOT_CAUSE_PROMPT
from vertexai.preview.generative_models import GenerativeModel
import vertexai

class SentimentalClassifierAgent:

    def __init__(self, project_id: str, location="us-central1"):
        aiplatform.init(project=project_id, location=location)
        model = GenerativeModel("gemini-2.0-flash")
        self.model = model

    def classify(self, case,track_messages):
        prompt = SENTIMENT_CLASSIFICATION_PROMPT.format(
            cases=case,
            track_messages=track_messages
        )

        response = self.model.generate_content(prompt)
        return response.text.replace("```json", "").replace("```", "").strip().lower()

    def caseToTrackId(self, case,track_messages):
        prompt = CASE_TO_TRACKING_ID_PROMPT.format(
            cases=case,
            track_messages=track_messages
        )

        response = self.model.generate_content(prompt)
        return response.text.replace("```json", "").replace("```", "").strip().lower()
    
    def getRootCause(self, case,track_messages):
        prompt = CASE_ROOT_CAUSE_PROMPT.format(
            cases=case,
            track_messages=track_messages
        )

        response = self.model.generate_content(prompt)
        return response.text.replace("```json", "").replace("```", "").strip().lower()
