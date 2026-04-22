#for pdfs
import fitz  # PyMuPDF
from app.core.log import logger
from app.core.errors import safe_execution
from app.db.file_repo import mark_processed
from app.core.utils import normalize_path

@safe_execution(component="EXTRACTOR",log_args=True)
def extract_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    logger.info("PDF has been extracted. Path:"+path)
    return text
