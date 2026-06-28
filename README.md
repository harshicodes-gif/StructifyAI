# Structify AI

> **Offline, CPU-First AI for Transforming Unstructured Documents into
> Structured Intelligence**

![License](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Offline-success.svg)
![Runtime](https://img.shields.io/badge/Inference-CPU--Only-green.svg)

## Overview

Structify AI is an offline-first AI application that converts
unstructured documents into structured, machine-readable data using
lightweight, CPU-optimized language models.

Unlike cloud-based document intelligence solutions, Structify AI
performs all processing locally on the user's device, ensuring privacy,
low latency, and uninterrupted operation even without an internet
connection.

The application is designed for environments where data privacy, offline
capability, and limited computing resources are critical.

------------------------------------------------------------------------

## Problem Statement

Organizations generate thousands of documents every day, including:

-   Maintenance Reports
-   Inspection Reports
-   Standard Operating Procedures (SOPs)
-   Service Reports
-   Incident Reports
-   Purchase Orders
-   Invoices

These documents contain valuable information but are typically stored as
unstructured text, making searching, reporting, and analytics difficult.

Manual data entry is time-consuming, error-prone, and expensive.

------------------------------------------------------------------------

## Solution

Structify AI automatically extracts key information from documents and
transforms it into structured JSON records that can be stored locally in
a SQLite database for future retrieval.

The entire pipeline runs offline using CPU-only inference.

``` text
Document/Image
        â”‚
        â–¼
OCR Extraction
        â”‚
        â–¼
Text Normalization
        â”‚
        â–¼
Local Small Language Model
        â”‚
        â–¼
Structured JSON
        â”‚
        â–¼
SQLite Database
```

## Key Features

-   Offline-first architecture
-   CPU-only AI inference
-   No cloud APIs
-   OCR for PDF and images
-   Intelligent information extraction
-   Structured JSON generation
-   Local SQLite storage
-   Searchable document history
-   JSON export
-   Graceful failure handling
-   Local caching for repeated documents

## Example

### Input

``` text
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

``` json
{
  "asset_id": "P-204",
  "asset_type": "Pump",
  "operator": "John Smith",
  "issue": "Bearing temperature exceeded threshold",
  "action_taken": "Bearing replaced",
  "downtime_minutes": 45
}
```

## Technology Stack

  Component           Technology
  ------------------- -----------------
  Frontend            Streamlit
  OCR                 EasyOCR
  Local LLM Runtime   llama.cpp
  Language Model      Qwen2.5 3B GGUF
  Validation          Pydantic
  Database            SQLite
  Packaging           PyInstaller
  Version Control     GitLab
  CI/CD               GitLab Runner

## Architecture

``` text
                Streamlit
                     â”‚
                     â–¼
          Upload PDF / Image
                     â”‚
                     â–¼
               EasyOCR
                     â”‚
                     â–¼
          Text Normalization
                     â”‚
                     â–¼
      Local LLM (llama.cpp)
                     â”‚
                     â–¼
         JSON Extraction Engine
                     â”‚
                     â–¼
        Pydantic Validation
                     â”‚
                     â–¼
               SQLite Storage
                     â”‚
                     â–¼
      Search / Export / History
```

## Project Structure

``` text
StructifyAI/
â”œâ”€â”€ app.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ README.md
â”œâ”€â”€ LICENSE
â”œâ”€â”€ CHANGELOG.md
â”œâ”€â”€ CONTRIBUTING.md
â”œâ”€â”€ .gitignore
â”œâ”€â”€ .gitlab-ci.yml
â”œâ”€â”€ src/
â”œâ”€â”€ tests/
â”œâ”€â”€ docs/
â”œâ”€â”€ uploads/
â”œâ”€â”€ outputs/
â”œâ”€â”€ cache/
â””â”€â”€ models/
```

## Installation

``` bash
git clone <repository-url>
cd StructifyAI

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Run

``` bash
streamlit run app.py
```

The application runs completely offline.

## Offline-First Design

-   Local inference only
-   CPU-first execution
-   No external API calls
-   Privacy-preserving processing
-   Local data persistence
-   Graceful degradation

## Future Enhancements

-   Handwritten document support
-   Audio transcription
-   Video frame extraction
-   Custom schema designer
-   Multi-language OCR
-   Batch processing

## Team

  -----------------------------------------------------------------------
  Name              Responsibilities
  ----------------- -----------------------------------------------------
  Harshita Kurella  Architecture, UI, Database, CI/CD, Documentation

  Buchammagari Adwitha   OCR, Local LLM Integration, Prompt Engineering,
                         Testing
  -----------------------------------------------------------------------

## License

GNU General Public License v3.0 (GPL-3.0).

See the LICENSE file for details.

## Acknowledgements

-   llama.cpp
-   EasyOCR
-   Streamlit
-   SQLite
-   Pydantic
-   GitLab