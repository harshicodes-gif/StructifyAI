# Structify AI Specification

## Project Name

**Structify AI – Offline CPU-First Document Intelligence System**

---

# Overview

Structify AI is an offline-first artificial intelligence application that converts unstructured documents into structured, machine-readable JSON records. The application is designed to work entirely on local machines using CPU-only inference without requiring cloud APIs or internet connectivity.

The system extracts information from scanned documents, PDFs, invoices, maintenance reports, inspection reports, SOPs, and service reports using OCR and a lightweight local language model. Extracted information is validated and stored in a local SQLite database for efficient searching and retrieval.

---

# Problem Statement

Organizations generate thousands of unstructured documents every day. Extracting useful information manually is slow, expensive, and prone to human error. Existing cloud-based document intelligence solutions often require internet connectivity and expose sensitive organizational data to third-party services.

There is a need for a secure, offline, privacy-preserving document intelligence solution that can run efficiently on standard CPU-based systems.

---

# Objectives

* Convert unstructured documents into structured JSON.
* Perform OCR on scanned PDFs and images.
* Run completely offline.
* Use lightweight CPU-optimized language models.
* Store extracted data locally.
* Provide searchable document history.
* Export structured results in JSON format.

---

# Target Users

* Manufacturing Companies
* Hospitals
* Government Departments
* Educational Institutions
* Small Businesses
* Maintenance Teams
* Field Engineers
* Quality Assurance Teams

---

# Functional Requirements

1. Upload PDF documents.
2. Upload image files (PNG, JPG, JPEG).
3. Perform OCR using EasyOCR.
4. Normalize extracted text.
5. Process text through a local language model.
6. Extract structured information in JSON format.
7. Validate JSON using Pydantic.
8. Store validated data in SQLite.
9. Search previously processed documents.
10. Export extracted records as JSON.

---

# Non-Functional Requirements

* Offline operation
* CPU-only execution
* Low memory usage
* Fast inference
* Privacy preservation
* Error handling
* Local caching
* Cross-platform compatibility
* Simple user interface

---

# System Architecture

Document Upload

↓

OCR Engine (EasyOCR)

↓

Text Normalization

↓

Local Language Model (llama.cpp + Qwen2.5 GGUF)

↓

JSON Extraction

↓

Pydantic Validation

↓

SQLite Database

↓

Search & Export

---

# Technology Stack

| Layer           | Technology      |
| --------------- | --------------- |
| Frontend        | Streamlit       |
| OCR             | EasyOCR         |
| Local LLM       | llama.cpp       |
| Language Model  | Qwen2.5 3B GGUF |
| Validation      | Pydantic        |
| Database        | SQLite          |
| Packaging       | PyInstaller     |
| CI/CD           | GitLab CI       |
| Version Control | GitLab          |

---

# User Workflow

1. Launch Structify AI.
2. Upload a document.
3. OCR extracts text.
4. Local LLM analyzes the content.
5. JSON is generated.
6. Data is validated.
7. Results are stored locally.
8. Users search or export previous records.

---

# Expected Input

* PDF
* JPG
* JPEG
* PNG

Supported documents include:

* Maintenance Reports
* Inspection Reports
* SOPs
* Purchase Orders
* Invoices
* Service Reports

---

# Expected Output

Structured JSON containing fields such as:

* Asset ID
* Asset Type
* Operator
* Issue
* Action Taken
* Downtime
* Timestamp

---

# Security

* No cloud APIs
* Offline processing
* Local SQLite database
* Documents remain on the user's device
* Privacy-first design

---

# Future Scope

* Multi-language OCR
* Batch processing
* Handwritten text recognition
* Audio transcription
* Video document extraction
* Custom schema designer
* CSV and Excel export

---

# Acceptance Criteria

* Uploading supported documents works successfully.
* OCR extracts readable text.
* Local LLM generates valid structured JSON.
* JSON passes validation.
* Data is stored in SQLite.
* Search functionality retrieves stored records.
* JSON export works correctly.
* The application functions completely offline.
* No external API calls are required.
* The application runs efficiently on CPU-only systems.
