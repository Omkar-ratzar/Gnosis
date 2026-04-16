from app.services.piepeline_service import process_documents
from app.config.config import config
from app.core.log import logger
limit= config["batch"]["file_processing_batch_size"]
def run():
    logger.info(f"[PIPELINE] Processing {limit} documents")
    process_documents(limit=limit)
