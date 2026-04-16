import docx2txt
from app.core.log import logger
from app.core.errors import safe_execution
from app.db.file_repo import mark_processed
from app.core.utils import normalize_path

@safe_execution(component="EXTRACTOR",log_args=True)
def extract_docx(path):
    text = docx2txt.process(path)
    mark_processed(normalize_path(path))
    logger.info("Docx has been extracted. Path:"+path)
    return (" ".join(text.split()))
