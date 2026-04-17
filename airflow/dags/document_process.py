#A DAG which will process all the document files: .doc .docx .pdf .txt .pptx,
from airflow.sdk import dag, task, Asset
from airflow.sdk.exceptions import AirflowSkipException
from app.config.config import config
from app.tasks.processing.validate import is_valid
from app.db.file_repo import mark_invalid, mark_processing,upsert_file
import os
from pendulum import datetime
# from app.services.piepeline_service import process_documents
from app.services.document_service import process_document
from app.config.config import config
from app.db.file_repo import get_new_documents
from File_Scan import new_docs_asset

# new_docs_asset = Asset("new_docs_ready")
limit= config["batch"]["file_processing_batch_size"]

@dag(dag_id="document_processor",
     start_date=datetime(2026, 1, 1),
     schedule=[new_docs_asset],
     catchup=False,
     tags=["gnosis", "scanner"]
     )
def doc_process():
    @task
    def fetch_files():
        files = get_new_documents(limit)
        if not files:
            raise AirflowSkipException("No new documents")
        return files

    @task(max_active_tis_per_dag=limit)
    def process_single(file):
        mark_processing(file["file_path"])
        process_document(file)

    files = fetch_files()
    process_single.expand(file=files) #Parallel execution per file

doc_process()


#This is very abstract rn but I will keep it as is for now, will break process_document into multiple tasks: text extraction, chunking, embedding for better vision but lets check this for now


