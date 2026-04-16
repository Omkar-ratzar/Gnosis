from app.services.piepeline_service import process_new_images
from app.config.config import config
from capp.ore.log import logger
from core.log import logger
limit= config["batch"]["image_processing_batch_size"]
def run():
    logger.info(f"[PIPELINE] Processing {limit} images")
    process_new_images(limit=limit)
