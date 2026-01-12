Multi-Modal Prompt Refinement System

A FastAPI-based backend and lightweight frontend that extracts unstructured content from multiple file types (including OCR images) and refines it into a clean, structured JSON prompt format suitable for AI pipelines.

This project is intentionally deterministic and rule-based, focusing on robust extraction, OCR noise handling, and explicit missing-information detection, rather than relying on LLM hallucinations.

✨ Key Features

📂 Upload multiple files at once

🖼️ OCR extraction from images using Tesseract

📄 Text extraction from PDF, DOCX, TXT

🧹 OCR noise cleaning & line normalization

🧠 Structured prompt refinement into JSON

⚠️ Explicit detection of missing or ambiguous information

🌐 Simple frontend for drag-and-drop uploads

🏗️ Project Structure
```
├── backend
│   ├── main.py                 # FastAPI app entry point
│   ├── processors              # File-type specific extractors
│   │   ├── dispatcher.py       # Routes files to correct processor
│   │   ├── image.py            # OCR extraction using Tesseract
│   │   ├── pdf.py              # PDF text extraction
│   │   ├── docx.py             # DOCX text extraction
│   │   └── text.py             # Plain text extraction
│   └── refiners
│       └── prompt_refiner.py   # Core prompt refinement logic
│
└── frontend
    ├── index.html              # UI for file upload
    ├── script.js               # API calls + JSON rendering
    └── style.css               # Basic styling
```
🧠 Prompt Refinement Output (JSON Schema)

Each uploaded file is transformed into the following structured format:

```
{
  "core_intent": "string",
  "functional_requirements": ["string"],
  "technical_constraints": ["string"],
  "expected_output": "string",
  "assumptions": ["string"],
  "missing_information": ["string"]
}
```

Why this structure?

Core Intent → What the document is fundamentally about

Functional Requirements → Business or user-facing goals

Technical Constraints → Technology, tools, platforms, or implementation details

Expected Output → Deliverables or results (if specified)

Assumptions → Notes, reminders, inferred intent

Missing Information → Explicit gaps (critical for AI reliability)

🔄 Data Flow

User uploads files via frontend

main.py receives files via FastAPI

dispatcher.py routes each file to the correct processor

Extracted raw text is passed to prompt_refiner.py

Refined JSON is returned to the frontend

Frontend renders structured output (cards / JSON view)


Refined Output:
```
{
  "core_intent": "Project Alpha - Q4 Goals",
  "functional_requirements": [
    "Launch new website",
    "Develop mobile app",
    "Expand to EU market",
    "Market research",
    "Content creation"
  ],
  "technical_constraints": [
    "UI/UX design mockups",
    "Backend setup"
  ],
  "expected_output": "",
  "assumptions": [],
  "missing_information": [
    "Expected output or deliverables are not explicitly mentioned"
  ]
}
```
🛠️ Tech Stack
Backend

Python 3.12

FastAPI

Tesseract OCR

Pillow

python-docx

PyPDF2

Frontend

HTML

Vanilla JavaScript

CSS

▶️ Running the Project
```
Backend
cd backend
uvicorn main:app --reload
```

Backend runs at:

```
http://localhost:8000
```
Frontend
```
Open directly:

frontend/index.html
```

(Or serve via a local static server if needed.)

🎯 Design Philosophy

No LLM dependency for parsing or structuring

Explicit over implicit (missing info is surfaced)

OCR-aware parsing (handles broken lines, merged columns, junk symbols)

Production-friendly JSON output

📌 Future Improvements

Layout-aware OCR (bounding boxes)

CSV / XLSX support

Confidence scoring per extracted item

Export refined prompts as downloadable JSON

