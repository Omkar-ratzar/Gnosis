from airflow.sdk import dag, task
from app.config.config import config
from app.tasks.processing.validate import is_valid
from app.db.file_repo import mark_invalid, mark_processing,upsert_file
import os
from pendulum import datetime

@dag(dag_id="file_scanner",
     start_date=datetime(2026, 1, 1),
     schedule="* * * * *",
     catchup=False,
     tags=["gnosis", "scanner"]
     )
def file_scan():
    @task
    def walk_dir():
        print("Scanning directory...")

        scan_path = config["paths"]["input_dir"]
        new_files = []

        for root, _, files in os.walk(scan_path):
            for file in files:
                full_path = os.path.join(root, file)
                new_files.append(full_path)
                upsert_file(full_path)
        return new_files


    @task
    def validate_files(files):
        # ti=kwargs['ti']
        # new_files=ti.xcom_pull(task_ids='walk_dir',key='return_result')['files']
        files_to_be_processed=files
        valid_files=[]
        invalid_files=[]
        for file in files_to_be_processed:
            if(is_valid(file)):
                valid_files.append(file)
            else:
                invalid_files.append(file)
                mark_invalid(file)
        return {
            "valid": valid_files,
            "invalid": invalid_files
        }

    
    validate_files(walk_dir())



file_scan()
