from fastapi import UploadFile
import pdfplumber
import tempfile

async def extract_pdf(file: UploadFile) -> str:
    text = ""
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(await file.read())
        tmp.flush()
        with pdfplumber.open(tmp.name) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    return text
