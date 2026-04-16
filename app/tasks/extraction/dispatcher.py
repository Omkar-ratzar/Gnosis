import os
from app.tasks.extraction.extract_pdf import extract_pdf
from app.tasks.extraction.extract_docx import extract_docx
from app.tasks.extraction.extract_pptx import extract_pptx

def extract_document(path: str):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return extract_pdf(path)
    elif ext == ".docx":
        return extract_docx(path)
    elif ext == ".pptx":
        return extract_pptx(path)
    elif ext == ".txt":
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    else:
        return None
