import re
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class CaseClassifier:
    def __init__(self):
        self.type_keywords = {
            'Incident': ['down', 'outage', 'crash', 'error', 'failure', 'not working', 'broken', 'critical', 'urgent'],
            'Bug': ['bug', 'defect', 'issue', 'wrong', 'incorrect', 'glitch', 'problem'],
            'Jira': ['task', 'story', 'epic', 'sprint', 'jira', 'ticket'],
            'Feature Request': ['feature', 'enhancement', 'improvement', 'add', 'new', 'want', 'need', 'request'],
            'Inquiry': ['how', 'what', 'when', 'where', 'why', 'question', 'help', 'info', 'documentation']
        }

        self.module_keywords = {
            'Authentication': ['login', 'password', 'auth', 'sign in', 'access', 'credential'],
            'Payment': ['payment', 'billing', 'invoice', 'charge', 'subscription', 'card'],
            'API': ['api', 'endpoint', 'integration', 'webhook', 'rest', 'graphql'],
            'Database': ['database', 'data', 'query', 'storage', 'backup', 'migration'],
            'UI/UX': ['interface', 'display', 'layout', 'design', 'button', 'screen', 'page'],
            'Performance': ['slow', 'performance', 'speed', 'latency', 'timeout', 'loading'],
            'Security': ['security', 'vulnerability', 'breach', 'encryption', 'ssl', 'https']
        }

    def classify_type(self, description: str) -> str:
        description_lower = description.lower()
        scores = {}

        for case_type, keywords in self.type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in description_lower)
            scores[case_type] = score

        if max(scores.values()) == 0:
            return 'Inquiry'

        return max(scores, key=scores.get)

    def classify_module(self, description: str) -> Tuple[str, str]:
        description_lower = description.lower()
        scores = {}

        for module, keywords in self.module_keywords.items():
            score = sum(1 for keyword in keywords if keyword in description_lower)
            scores[module] = score

        if max(scores.values()) == 0:
            module = 'General'
            sub_module = 'Other'
        else:
            module = max(scores, key=scores.get)
            sub_module = f"{module} Support"

        return module, sub_module

    def assign_category(self, case_type: str, priority: str) -> str:
        if priority == 'Critical':
            return 'P0 - Critical'
        elif priority == 'High':
            return 'P1 - High Priority'
        elif case_type == 'Incident':
            return 'P2 - Incident'
        elif case_type == 'Bug':
            return 'P2 - Bug Fix'
        else:
            return 'P3 - Standard'

class SimilarityDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.case_vectors = None
        self.case_ids = []

    def fit(self, cases: List[dict]):
        if not cases:
            return

        descriptions = [case['description'] for case in cases]
        self.case_ids = [case['id'] for case in cases]
        self.case_vectors = self.vectorizer.fit_transform(descriptions)

    def find_similar(self, case_description: str, case_id: str = None, top_k: int = 3) -> List[Tuple[str, float]]:
        if self.case_vectors is None or len(self.case_ids) == 0:
            return []

        query_vector = self.vectorizer.transform([case_description])
        similarities = cosine_similarity(query_vector, self.case_vectors)[0]

        similar_indices = similarities.argsort()[-top_k-1:][::-1]

        results = []
        for idx in similar_indices:
            if self.case_ids[idx] != case_id:
                results.append((self.case_ids[idx], float(similarities[idx])))
                if len(results) == top_k:
                    break

        return results
