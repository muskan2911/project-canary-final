from google.cloud import bigquery
from typing import List, Optional
import os

class Database:
    def __init__(self):
        self.project = 'sab-dev-nghp-jobs-4063'
        self.dataset = 'project_canary'
        self.table = 'cases'
        self.table_ref = f'{self.project}.{self.dataset}.{self.table}'
        self.client = bigquery.Client(project=self.project)

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
        query = f"""
            SELECT similar_case_url
            FROM `{self.table_ref}`
            WHERE case_id = @case_id AND similar_case_url IS NOT NULL AND similar_case_url != ''
            LIMIT {limit}
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("case_id", "STRING", case_id)
            ]
        )
        results = [dict(row) for row in self.client.query(query, job_config=job_config).result()]
        return results

    def update_case_by_id(self, case_id: str, updates: dict) -> Optional[dict]:
        # Build SET clause and parameters
        set_clauses = []
        params = [bigquery.ScalarQueryParameter("case_id", "STRING", case_id)]
        for key, value in updates.items():
            set_clauses.append(f"{key} = @{key}")
            params.append(bigquery.ScalarQueryParameter(key, "STRING", value))
        if not set_clauses:
            return None
        set_clause = ", ".join(set_clauses)
        query = f"UPDATE `{self.table_ref}` SET {set_clause} WHERE case_id = @case_id"
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        self.client.query(query, job_config=job_config).result()
        # Return updated case
        return self.get_case_by_id(case_id)

    def add_comment_to_case(self, case_id: str, comment: str) -> Optional[dict]:
        # Fetch current comments
        case = self.get_case_by_id(case_id)
        if not case:
            return None
        current_comments = case.get('comments') or ''
        # Append new comment (newline separated)
        if current_comments:
            updated_comments = current_comments + '\n' + comment
        else:
            updated_comments = comment
        # Update in DB
        query = f"UPDATE `{self.table_ref}` SET comments = @comments WHERE case_id = @case_id"
        job_config = bigquery.QueryJobConfig(query_parameters=[
            bigquery.ScalarQueryParameter("comments", "STRING", updated_comments),
            bigquery.ScalarQueryParameter("case_id", "STRING", case_id)
        ])
        self.client.query(query, job_config=job_config).result()
        return self.get_case_by_id(case_id)

    def create_track(self, track_name: str) -> dict:
        track_table = f'{self.project}.{self.dataset}.track'
        query = f"""
            INSERT INTO `{track_table}` (track_id, track_name)
            VALUES (GENERATE_UUID(), @track_name)
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("track_name", "STRING", track_name)]
        )
        self.client.query(query, job_config=job_config).result()
        # Fetch the newly created track
        query = f"SELECT * FROM `{track_table}` WHERE track_name = @track_name ORDER BY track_id DESC LIMIT 1"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("track_name", "STRING", track_name)]
        )
        result = list(self.client.query(query, job_config=job_config).result())
        return dict(result[0]) if result else {}

    def delete_track(self, track_id: str):
        track_table = f'{self.project}.{self.dataset}.track'
        query = f"DELETE FROM `{track_table}` WHERE track_id = @track_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("track_id", "STRING", track_id)]
        )
        self.client.query(query, job_config=job_config).result()

    def list_tracks(self) -> list:
        track_table = f'{self.project}.{self.dataset}.track'
        query = f"SELECT * FROM `{track_table}` ORDER BY track_id DESC"
        return [dict(row) for row in self.client.query(query).result()]

    def assign_track_to_case(self, track_id: str, case_id: str):
        map_table = f'{self.project}.{self.dataset}.case_track_map'
        query = f"""
            INSERT INTO `{map_table}` (case_id, track_id)
            VALUES (@case_id, @track_id)
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("case_id", "STRING", case_id),
                bigquery.ScalarQueryParameter("track_id", "STRING", track_id)
            ]
        )
        self.client.query(query, job_config=job_config).result()

    def get_cases_for_track(self, track_id: str) -> list:
        map_table = f'{self.project}.{self.dataset}.case_track_map'
        query = f"SELECT case_id FROM `{map_table}` WHERE track_id = @track_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("track_id", "STRING", track_id)]
        )
        return [dict(row) for row in self.client.query(query, job_config=job_config).result()]
