from app.db.image_repo import mark_processed_metadata
from app.db.image_repo import mark_processing_metadata
from app.db.image_repo import upsert_image_metadata
from app.tasks.processing.chunk_text import chunk_text
from app.tasks.embedding.embed_chunks import embed_chunks
from app.tasks.embedding.vector_store import upsert_vectors, init_collection
from app.db.file_repo import mark_processed
from app.tasks.extraction.extract_image import extract_image
from app.tasks.extraction.extract_exif import extract_exif
from app.core.log import logger
from app.config.config import config
import uuid
import json


def process_image(file):
    # DB state handled here
    logger.info(f"[SERVICE] Processing {file['file_id']} image")

    mark_processing_metadata(file["file_id"])
    desc = extract_image(file["file_path"])
    exif = extract_exif(file["file_path"])
    upsert_image_metadata(file["file_id"], file["file_path"], desc, exif)
    mark_processed_metadata(file["file_id"])
    mark_processed(file["file_path"])


    desc = desc or ""
    exif = json.dumps(exif, ensure_ascii=False) or {}
    text = f"{desc}\n{exif}"


    chunk_size = config["chunking"]["chunk_size"]
    overlap = config["chunking"]["overlap"]

    chunks = chunk_text(text, chunk_size, overlap)
    if not chunks:
        print(f"[WARN] No chunks: {file['file_path']}")
        return
    vectors = embed_chunks(chunks)

    if vectors is None or vectors.shape[0] == 0:
        print(f"[WARN] No vectors for file: {file['file_path']}")
        return

    init_collection(dim=len(vectors[0]))

    ids = []
    payloads = []

    for i, chunk in enumerate(chunks):
        ids.append(str(uuid.uuid4()))
        payloads.append({
            "file_id": file["file_id"],
            "file_name": file["file_path"],
            "text": chunk
        })

    upsert_vectors(ids, vectors, payloads)

