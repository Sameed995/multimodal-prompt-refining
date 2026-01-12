from fastapi import UploadFile
from .text import extract_txt
from .pdf import extract_pdf
from .docx import extract_docx
from .image import extract_image

async def extract_content(file: UploadFile) -> dict:
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        text = await extract_txt(file)
        file_type = "txt"

    elif filename.endswith(".pdf"):
        text = await extract_pdf(file)
        file_type = "pdf"

    elif filename.endswith(".docx"):
        text = await extract_docx(file)
        file_type = "docx"
    
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        text = await extract_image(file)
        file_type = "image"

    else:
        raise ValueError("Unsupported file type")

    return {
        "filename": file.filename,
        "type": file_type,
        "extracted_text": text
    }
