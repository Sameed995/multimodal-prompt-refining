from fastapi import UploadFile
from docx import Document
import tempfile

async def extract_docx(file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=True, suffix=".docx") as tmp:
        tmp.write(await file.read())
        tmp.flush()
        document = Document(tmp.name)
        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]

    return "\n".join(paragraphs)
