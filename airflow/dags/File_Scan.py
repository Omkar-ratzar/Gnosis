from airflow.sdk import dag, task, Asset
from airflow.sdk.exceptions import AirflowSkipException
from app.config.config import config
from app.tasks.processing.validate import is_valid
from app.db.file_repo import mark_invalid, mark_processing,upsert_file,get_file_id_by_path
from app.db.image_repo import upsert_image_metadata
import os
from pendulum import datetime

##OPTIMIZATION TO BE NOTED, this runs every minute and processes every file, next I will process only the files which do not exist in my DB.

#hard coding in vector_db and extract_image for testing purposes, will fix env import later on

#declaring 'Assets', so I can use them as a trigger for other dags
new_docs_asset = Asset("new_docs_ready")
new_images_asset = Asset("new_images_ready")


IMAGE_EXTS = (".jpg", ".jpeg", ".png")
DOC_EXTS = (".pdf", ".docx", ".pptx", ".txt")


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
                print(full_path)
        return new_files

    @task(outlets=[new_docs_asset])
    def validate_docs(files):
        valid, invalid = [], []
        for f in files:
            if f.lower().endswith(DOC_EXTS) and is_valid(f):
                valid.append(f)
            elif f.lower().endswith(DOC_EXTS):
                invalid.append(f)
                mark_invalid(f)
        if not valid:
            raise AirflowSkipException("No valid docs found, skipping asset emit")

        return {"valid": valid, "invalid": invalid}

    @task(outlets=[new_images_asset])
    def validate_images(files):
        valid, invalid = [], []
        for f in files:
            if f.lower().endswith(IMAGE_EXTS) and is_valid(f):
                valid.append(f)
                print(f)
                file_id = get_file_id_by_path(f)
                if file_id:
                    upsert_image_metadata(
                        file_id, f, None, None, status="NEW"
                    )
            elif f.lower().endswith(IMAGE_EXTS):
                invalid.append(f)
                mark_invalid(f)
        if not valid:
            raise AirflowSkipException("No valid imgs found, skipping asset emit")

        return {"valid": valid, "invalid": invalid}

    walked = walk_dir()
    validate_docs(walked)
    validate_images(walked)

file_scan()
