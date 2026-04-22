from app.tasks.extraction.dispatcher import extract_document
from app.tasks.processing.chunk_text import chunk_text
from app.tasks.embedding.embed_chunks import embed_chunks
from app.tasks.embedding.vector_store import upsert_vectors, init_collection,delete_vectors_by_file_id
from app.core.log import logger
from app.db.file_repo import mark_processed
from app.config.config import config
from app.core.utils import normalize_path

import uuid

def process_document(file):
    text = extract_document(file["file_path"])
    print("FILE:", file["file_path"])
    print("TEXT LEN:", len(text) if text else 0)
    logger.info(f"[SERVICE] Processing {file['file_id']} document")
    if not text:
        logger.error(f"[SERVICE] EXTRACTION FAILED IN document_service.py for {file['file_id']}")
        return
    # return text

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
        ids.append(str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{file['file_id']}_{i}")))
        payloads.append({
            "file_id": file["file_id"],
            "file_name": file["file_path"],
            "text": chunk
        })
    if not ids:
        logger.error(f"No valid IDs/chunks for file {file['file_id']}, skipping delete/upsert")
        return
    try:
        delete_vectors_by_file_id(file["file_id"])
        upsert_vectors(ids, vectors, payloads)
        mark_processed(["file_path"])

    except Exception as e:
        logger.error(f"Vector upsert failed for {file['file_id']}: {e}")
        raise
