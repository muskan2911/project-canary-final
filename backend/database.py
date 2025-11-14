from google.cloud import bigquery
from typing import List, Optional
import os

class Database:
    def __init__(self):
        self.client = bigquery.Client()
        self.dataset = 'project_canary'
        self.table = 'cases'
        self.table_ref = f'{self.dataset}.{self.table}'

    def get_all_cases(self) -> List[dict]:
        query = f"SELECT * FROM `{self.table_ref}` ORDER BY created_date DESC"
        return [dict(row) for row in self.client.query(query).result()]

    def get_case_count(self) -> int:
        query = f"SELECT COUNT(*) as total FROM `{self.table_ref}`"
        result = self.client.query(query).result()
        return list(result)[0]['total']

    def get_cases_by_priority(self, priority: str) -> List[dict]:
        query = f"SELECT * FROM `{self.table_ref}` WHERE priority = @priority ORDER BY created_date DESC"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("priority", "STRING", priority)]
        )
        return [dict(row) for row in self.client.query(query, job_config=job_config).result()]

    def get_cases_by_type(self, case_type: str) -> List[dict]:
        query = f"SELECT * FROM `{self.table_ref}` WHERE type = @type ORDER BY created_date DESC"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("type", "STRING", case_type)]
        )
        return [dict(row) for row in self.client.query(query, job_config=job_config).result()]

    def get_cases_by_status(self, status: str) -> List[dict]:
        query = f"SELECT * FROM `{self.table_ref}` WHERE status = @status ORDER BY created_date DESC"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("status", "STRING", status)]
        )
        return [dict(row) for row in self.client.query(query, job_config=job_config).result()]

    def search_cases(self, customer_name: Optional[str] = None, case_id: Optional[str] = None,
                    product: Optional[str] = None, priority: Optional[str] = None,
                    case_type: Optional[str] = None) -> List[dict]:
        conditions = []
        params = []
        if customer_name:
            conditions.append("customer_name LIKE @customer_name")
            params.append(bigquery.ScalarQueryParameter("customer_name", "STRING", f"%{customer_name}%"))
        if case_id:
            conditions.append("case_id LIKE @case_id")
            params.append(bigquery.ScalarQueryParameter("case_id", "STRING", f"%{case_id}%"))
        if product:
            conditions.append("product = @product")
            params.append(bigquery.ScalarQueryParameter("product", "STRING", product))
        if priority:
            conditions.append("priority = @priority")
            params.append(bigquery.ScalarQueryParameter("priority", "STRING", priority))
        if case_type:
            conditions.append("type = @type")
            params.append(bigquery.ScalarQueryParameter("type", "STRING", case_type))
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        query = f"SELECT * FROM `{self.table_ref}` WHERE {where_clause} ORDER BY created_date DESC"
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        return [dict(row) for row in self.client.query(query, job_config=job_config).result()]

    def insert_case(self, case_data: dict):
        errors = self.client.insert_rows_json(self.table_ref, [case_data])
        if errors:
            raise Exception(f"BigQuery insert error: {errors}")

    def get_case_by_id(self, case_id: str) -> Optional[dict]:
        query = f"SELECT * FROM `{self.table_ref}` WHERE case_id = @case_id LIMIT 1"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("case_id", "STRING", case_id)]
        )
        result = list(self.client.query(query, job_config=job_config).result())
        return dict(result[0]) if result else None

    def insert_cases_batch(self, cases: List[dict]):
        errors = self.client.insert_rows_json(self.table_ref, cases)
        if errors:
            raise Exception(f"BigQuery batch insert error: {errors}")
        return cases

    def insert_similarity(self, case_id: str, related_case_id: str, similarity_score: float):
        similarity_table = f'{self.dataset}.case_similarity'
        row = {
            'id': f'{case_id}_{related_case_id}',
            'case_id': case_id,
            'related_case_id': related_case_id,
            'similarity_score': similarity_score,
            'created_date': bigquery._helpers._datetime_to_json()
        }
        errors = self.client.insert_rows_json(similarity_table, [row])
        if errors:
            raise Exception(f"BigQuery similarity insert error: {errors}")

    def delete_similarities_for_case(self, case_id: str):
        query = f"DELETE FROM `{self.dataset}.case_similarity` WHERE case_id = @case_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("case_id", "STRING", case_id)]
        )
        self.client.query(query, job_config=job_config).result()

    def get_dashboard_stats(self):
        query = f"""
        SELECT
            COUNT(*) AS total_cases,
            SUM(CASE WHEN priority = 'High' OR priority = 'Critical' THEN 1 ELSE 0 END) AS high_priority,
            SUM(CASE WHEN type = 'Incident' THEN 1 ELSE 0 END) AS incidents,
            SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) AS open_cases
        FROM `{self.table_ref}`
        """
        result = list(self.client.query(query).result())[0]
        return {
            'total_cases': result['total_cases'],
            'high_priority': result['high_priority'],
            'incidents': result['incidents'],
            'open_cases': result['open_cases']
        }

    def get_similar_cases(self, case_id: str, limit: int = 3) -> List[dict]:
        similarity_table = f'{self.dataset}.case_similarity'
        query = f"""
            SELECT related_case_id, similarity_score
            FROM `{similarity_table}`
            WHERE case_id = @case_id
            ORDER BY similarity_score DESC
            LIMIT {limit}
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("case_id", "STRING", case_id)
            ]
        )
        results = [dict(row) for row in self.client.query(query, job_config=job_config).result()]
        # Optionally fetch full case details for each related_case_id
        similar_cases = []
        for row in results:
            related_case = self.get_case_by_id(row['related_case_id'])
            if related_case:
                related_case['similarity_score'] = row['similarity_score']
                similar_cases.append(related_case)
        return similar_cases
