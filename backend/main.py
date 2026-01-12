from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from typing_extensions import Annotated

from backend.processors.dispatcher import extract_content
from backend.refiners.prompt_refiner import refine_prompt

app = FastAPI(
    title="Multi-Modal Prompt Refinement Backend",
    description="Backend API for extracting and refining prompts from uploaded files",
    version="1.0"
)

# cors configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/refine-prompt")
async def refine_prompt_endpoint(
    files: Annotated[
        List[UploadFile],
        File(description="Upload multiple files (txt, pdf, docx, images)")
    ]
):

    results = []

    for file in files:
        try:
           
            extracted = await extract_content(file)
            is_image = extracted["type"] == "image"
            refined = refine_prompt(extracted["extracted_text"], is_image=is_image)
            results.append({
                "filename": extracted["filename"],
                "file_type": extracted["type"],
                "extracted_text": extracted["extracted_text"],  # raw OCR / text
                "refined_prompt": refined
            })

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing {file.filename}: {str(e)}"
            )

    return {
        "message": "Prompt refined successfully",
        "results": results
    }
