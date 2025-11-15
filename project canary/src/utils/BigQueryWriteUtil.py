from google.cloud import bigquery
import random


class BigQueryWriteUtil:
    def insert(sample_case,type_agent_output,product_agent_output,sentimental_agent_output,case_grouping_agent_output,case_to_track_id_mapping,root_cause_mapping):
        client = bigquery.Client("sab-dev-nghp-jobs-4063")

        # Define your dataset and table
        dataset_id = "project_canary"
        table_id_cases = "cases"
        table_id_case_to_track = "case_track_map"
        table_ref_cases = client.dataset(dataset_id).table(table_id_cases)
        table_ref_cases_track_map = client.dataset(dataset_id).table(table_id_case_to_track)

        # Prepare data (list of dictionaries)
        rows_to_insert_cases = []
        for case in sample_case:
            cid = case["id"].lower()
            print(cid)
            merged = {
                "case_id": cid,
                "customer_name": case["name"],
                "priority": sentimental_agent_output.get(cid.lower()),
                "type":type_agent_output.get(cid.lower()),
                "product":product_agent_output.get(cid.lower()),
                "status":case["status"],
                "description":case["description"],  
                "module":None,
                "sub_module":None,
                "category":"P3",
                "similar_case_url": ",".join([v for v in (case_grouping_agent_output.get(cid.lower()) or []) if v.lower() != "none"]),
                "created_date" : case["created_date"],
                "geography":None,
                "comments":None,
                "jira_id":None if random.choice([True, False]) else "PTJIRA" + str(random.randint(1, 9999)),
                "snow_id":None if random.choice([True, False]) else "INC" + str(random.randint(10000, 99999)),
                "mail_chain":None,
                "ROOTCAUSE":root_cause_mapping.get(cid.lower())
            }
            rows_to_insert_cases.append(merged)
               
       
        rows_to_insert_cases_track = []
        for case in sample_case:
            cid = case["id"].lower()
            merged= {
                "case_id": cid,
                "track_id": case_to_track_id_mapping.get(cid.lower())
            }
            rows_to_insert_cases_track.append(merged)

        
        errors = client.insert_rows_json(table_ref_cases, rows_to_insert_cases)
        errors = client.insert_rows_json(table_ref_cases_track_map, rows_to_insert_cases_track)
        if errors == []:
            print("Data pushed successfully!")
        else:
            print("Data pushed failed!")


