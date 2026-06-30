---
title: Structify AI
emoji: 📄
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.58.0"
python_version: "3.11"
app_file: app.py
pinned: false
---
# Structify AI

> **Offline, CPU-First AI for Transforming Unstructured Documents into Structured Intelligence**

![License](https://img.shields.io/badge/License-AGPLv3-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Offline-success.svg)
![Runtime](https://img.shields.io/badge/Inference-CPU--Only-green.svg)
![CI](https://img.shields.io/badge/CI-GitLab-orange.svg)

---

## Overview

Structify AI is an **offline-first AI application** that transforms unstructured documents into structured, machine-readable data using lightweight, CPU-optimized language models.

Unlike cloud-based document intelligence solutions, Structify AI performs every step locally on the user's device, ensuring:

* Complete privacy
* Low latency
* Offline operation
* Zero cloud dependency

The application is designed for environments where data privacy, limited computing resources, and offline availability are essential.

---

## Demo

> Add your application screenshot here.

```text
docs/demo.png
```

---

## Problem Statement

Organizations generate thousands of documents every day, including:

* Maintenance Reports
* Inspection Reports
* Standard Operating Procedures (SOPs)
* Service Reports
* Incident Reports
* Purchase Orders
* Invoices

These documents contain valuable information but are usually stored as unstructured text.

As a result:

* Information is difficult to search.
* Manual data entry is slow.
* Human errors are common.
* Reporting and analytics become difficult.

---

## Solution

Structify AI automatically extracts important information from uploaded documents and converts it into structured JSON records that are validated and stored locally in a SQLite database.

The complete processing pipeline runs **100% offline** using CPU-only inference.

```text
Document / Image
        │
        ▼
OCR Extraction
        │
        ▼
Text Normalization
        │
        ▼
Local Language Model
        │
        ▼
Structured JSON
        │
        ▼
SQLite Database
```

---

## Key Features

* Offline-first architecture
* CPU-only AI inference
* No cloud APIs
* OCR support for PDF and images
* Intelligent information extraction
* Structured JSON generation
* SQLite local database
* Searchable document history
* JSON export
* Local document caching
* Error handling and validation
* Fast processing on standard laptops

---

## Supported Documents

* PDF
* PNG
* JPG
* JPEG
* Maintenance Reports
* Inspection Reports
* Service Reports
* SOP Documents
* Purchase Orders
* Invoices

---

## Why Structify AI?

* 100% Offline
* Privacy First
* CPU Optimized
* Lightweight
* Easy Deployment
* Open Source
* No Internet Required

---

## Example

### Input

```text
Machine: Pump P-204

Operator: John Smith

Issue:
Bearing temperature exceeded threshold.

Action:
Bearing replaced.

Downtime:
45 minutes.
```

### Output

```json
{
  "asset_id": "P-204",
  "asset_type": "Pump",
  "operator": "John Smith",
  "issue": "Bearing temperature exceeded threshold",
  "action_taken": "Bearing replaced",
  "downtime_minutes": 45
}
```

---

## Technology Stack

| Component         | Technology      |
| ----------------- | --------------- |
| Frontend          | Streamlit       |
| OCR               | EasyOCR         |
| Local LLM Runtime | llama.cpp       |
| Language Model    | Qwen2.5 3B GGUF |
| Validation        | Pydantic        |
| Database          | SQLite          |
| Packaging         | PyInstaller     |
| Version Control   | GitLab          |
| CI/CD             | GitLab Runner   |

---

## Architecture

```text
                Streamlit
                    │
                    ▼
          Upload PDF / Image
                    │
                    ▼
               EasyOCR
                    │
                    ▼
         Text Normalization
                    │
                    ▼
      Local LLM (llama.cpp)
                    │
                    ▼
     JSON Extraction Engine
                    │
                    ▼
      Pydantic Validation
                    │
                    ▼
          SQLite Storage
                    │
                    ▼
      Search • Export • History
```

---

## Project Structure

```text
StructifyAI/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── .gitignore
├── .gitlab-ci.yml
├── src/
├── tests/
├── docs/
├── uploads/
├── outputs/
├── cache/
└── models/
```

---

## Installation

```bash
git clone <repository-url>

cd StructifyAI

python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

The application runs completely offline.

---

## Offline-First Design

* Local inference only
* CPU-first execution
* No external API calls
* Privacy-preserving processing
* Local data persistence
* Graceful degradation

---

## Performance

* Optimized for CPU execution
* Lightweight inference
* Local caching
* Fast startup
* Minimal memory usage

---

## Security

* Documents never leave the local machine
* No internet dependency
* Local SQLite storage
* No third-party APIs
* Fully private processing

---

## Future Enhancements

* Handwritten document recognition
* Batch document processing
* Audio transcription
* Video frame extraction
* Custom schema designer
* Multi-language OCR
* CSV and Excel export
* Advanced document search

---

## Repository Health

* README
* LICENSE
* CHANGELOG
* CONTRIBUTING Guide
* GitLab CI/CD
* Unit Tests
* Issue Templates
* Code Quality Checks

---

## Team

| Name                 | Responsibilities                                                    |
| -------------------- | ------------------------------------------------------------------- |
| Harshita Kurella     | Architecture, UI, Database, CI/CD, Documentation                    |
| Buchammagari Adwitha | OCR Integration, Local LLM Integration, Prompt Engineering, Testing |

---

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See the **LICENSE** file for more information.

---

## Acknowledgements

Special thanks to the following open-source projects:

* llama.cpp
* EasyOCR
* Streamlit
* SQLite
* Pydantic
* GitLab
* Qwen2.5 GGUF Models

---

**Structify AI — Transforming Unstructured Documents into Structured Intelligence, Completely Offline.**
