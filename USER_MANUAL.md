# Structify AI User Manual

## Overview

Structify AI converts uploaded PDF and image documents into structured JSON
records using local OCR, local model inference, validation, and SQLite storage.
The application is designed to run offline on CPU-only machines.

## Prerequisites

* Python 3.11 or newer
* A local virtual environment
* Project dependencies installed from `requirements.txt`
* Optional local GGUF model files stored outside version control

## Installation

```bash
git clone <repository-url>
cd StructifyAI
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Activate the environment on Linux or macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Starting the Application

```bash
streamlit run app.py
```

After Streamlit starts, open the local URL shown in the terminal.

## Uploading Documents

1. Open the Upload page.
2. Select a supported file type: PDF, PNG, JPG, or JPEG.
3. Start processing.
4. Review the extracted text and generated JSON output.
5. Save or export the structured result when it is valid.

## Viewing History

Use the History page to review previously processed documents stored in the
local SQLite database. History is stored locally and is not sent to an external
service.

## Settings

Use the Settings page to review runtime preferences, local paths, and processing
options exposed by the application.

## Data Privacy

Structify AI is offline-first. Uploaded documents, extracted text, generated
JSON, and SQLite data remain on the local machine unless a user manually exports
or shares them.

## Troubleshooting

* If the application fails to start, confirm the virtual environment is active
  and dependencies are installed.
* If OCR fails, confirm the uploaded document is a supported format and readable.
* If model inference is unavailable, confirm the local model path is configured
  correctly.
* If database writes fail, confirm the application has permission to write to
  the project data directory.

## Maintenance Commands

```bash
ruff check .
black --check .
mypy app.py backend frontend
pytest
bandit -r app.py backend frontend -x tests,.venv,venv
```
