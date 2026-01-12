from fastapi import UploadFile
from PIL import Image
import pytesseract
import io


async def extract_image(file: UploadFile) -> str:
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    text = pytesseract.image_to_string(image)
    return text
