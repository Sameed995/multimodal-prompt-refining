Note: This project was made completely locally and the final version was pushed, hence no git history
# Multi-Modal Prompt Refinement System

A FastAPI-based backend and lightweight frontend that extracts unstructured content from multiple file types such as text, docx, pdf, and images (ocr) and refines it into a clean, structured JSON prompt format suitable for AI pipelines.

This project is **intentionally deterministic and rule-based**, focusing on robust extraction, OCR noise handling, and explicit missing-information detection, rather than relying on LLM hallucinations.

---

## Key Features

- 📂 **Upload multiple files at once**
- 🖼️ **OCR extraction from images** using Tesseract
- 📄 **Text extraction** from PDF, DOCX, TXT
- 🧹 **OCR noise cleaning** & line normalization
- 🧠 **Structured prompt refinement** into JSON
- ⚠️ **Explicit detection** of missing or ambiguous information
- 🌐 **Simple frontend** for drag-and-drop uploads

---

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── processors/             # File-type specific extractors
│   │   ├── dispatcher.py       # Routes files to correct processor
│   │   ├── image.py            # OCR extraction using Tesseract
│   │   ├── pdf.py              # PDF text extraction
│   │   ├── docx.py             # DOCX text extraction
│   │   └── text.py             # Plain text extraction
│   └── refiners/
│       └── prompt_refiner.py   # Core prompt refinement logic
│
└── frontend/
    ├── index.html              # UI for file upload
    ├── script.js               # API calls + JSON rendering
    └── style.css               # Basic styling
```

---

## Prompt Refinement Output (JSON Schema)

Each uploaded file is transformed into the following structured format:

```json
{
  "core_intent": "string",
  "functional_requirements": ["string"],
  "technical_constraints": ["string"],
  "expected_output": "string",
  "assumptions": ["string"],
  "missing_information": ["string"]
}
```

### Why this structure?

- **`core_intent`** → What the document is fundamentally about
- **`functional_requirements`** → Business or user-facing goals
- **`technical_constraints`** → Technology, tools, platforms, or implementation details
- **`expected_output`** → Deliverables or results (if specified)
- **`assumptions`** → Notes, reminders, inferred intent
- **`missing_information`** → Explicit gaps (critical for AI reliability)

---

## Data Flow

1. User uploads files via frontend
2. `main.py` receives files via FastAPI
3. `dispatcher.py` routes each file to the correct processor
4. Extracted raw text is passed to `prompt_refiner.py`
5. Refined JSON is returned to the frontend
6. Frontend renders structured output (cards / JSON view)

### Example Input

```
Project Alpha - Q4 Goals
- Launch new website
- Develop mobile app
- Expand to EU market
TODO: Market research, content creation
Technical: UI/UX design mockups, backend setup
```

### Refined Output

```json
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

---

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- Tesseract OCR
- Pillow
- python-docx
- PyPDF2

### Frontend
- HTML
- Vanilla JavaScript
- CSS

---

## ▶ Running the Project

### Prerequisites

Ensure you have the following installed:
- Python 3.12+
- Tesseract OCR ([installation guide](https://github.com/tesseract-ocr/tesseract))
- pip (Python package manager)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn pillow python-docx PyPDF2 pytesseract
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

Backend runs at: **`http://localhost:8000`**

### Frontend Setup

Simply open the frontend HTML file in your browser:

```bash
cd frontend
open index.html
```

Or serve it using a local static server if needed:

```bash
python -m http.server 3000
```

Then navigate to: **`http://localhost:3000`**

---

## Design Philosophy

- **No LLM dependency** for parsing or structuring
- **Explicit over implicit** (missing info is surfaced)
- **OCR-aware parsing** (handles broken lines, merged columns, junk symbols)
- **Production-friendly JSON output**

This approach ensures reliability, predictability, and transparency in content extraction and structuring, making it ideal for AI pipelines that require high-quality, validated inputs.

---

## 📌 Future Improvements

- [ ] CSV / XLSX support
- [ ] Confidence scoring per extracted item
- [ ] Export refined prompts as downloadable JSON
- [ ] Support for additional file formats (Markdown, HTML)
- [ ] API documentation with Swagger/OpenAPI

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).

---

## 📧 Contact

For questions or feedback, please open an issue or reach out via the repository's discussion board.