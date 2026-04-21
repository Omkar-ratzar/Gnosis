# Gnosis

A Next-Generation Multimodal Semantic Search Pipeline Orchestrated with Apache Airflow.

## Vision
The goal is to make unstructured data easily searchable without manual tagging or strict organization.

Real-world storage systems become messy over time. Gnosis automatically understands and indexes content—documents and images—turning raw data into a searchable knowledge base.

## Complete Architecture Revamp
Gnosis has transitioned from a basic file-system watchdog model to a robust, **Apache Airflow-based orchestration** system. This iteration guarantees reliable pipelines, robust retry mechanisms, scalable processing, and transparent visual monitoring.

The core processing logic is cleanly decoupled and served seamlessly through an interactive API and frontend web UI.

## How It Works

Gnosis operates seamlessly using dedicated processing pipelines and robust backing services:

### 1. Robust File Ingestion
- Files are securely uploaded through the FastAPI-powered backend (`/api/upload`).
- Artifacts securely store in `app/data/` prior to pipeline ingestion.

### 2. Airflow Orchestration and Pipelines
- Replaced legacy watchdog.py tracking by stringing together ingestion and computation tasks into reliable DAGs (`airflow/dags`).
- Orchestrates explicit processing pathways via Document (`run_docs`) and Image (`run_images`) Pipelines.

### 3. Image Preprocessing & Understanding
- Generates structured descriptions (via MiniCPM-V and Ollama).
- Aggregates and stores EXIF metadata.
- Connects non-textual image features into searchable semantic fields.

### 4. Comprehensive Document Extraction
- Supports multi-format text extraction mechanisms:
  - **PDF** → PyMuPDF
  - **DOCX** → docx2txt
  - **PPTX** → python-pptx
  - **TXT** → Native reads

### 5. Advanced Chunking & Embeddings
- Decomposes massive structural text into cohesive, overlapping context chunks.
- Maps raw text blocks into dense vector spaces using (`BAAI/bge-small-en-v1.5`).

### 6. Sub-millisecond Storage & Search
- Standard relational metadata and states secured via PostgreSQL.
- Heavy-duty vector indexing and distance calculations using Qdrant.
- Cosine-similarity searches pushed live over our search API endpoints (`/api/search`).

## Tech Stack

- **Backend / Delivery:** FastAPI, Uvicorn, Python 3.11+
- **Orchestration:** Apache Airflow
- **Machine Learning / AI:** SentenceTransformers, Ollama (minicpm-v), PyTorch
- **Data Persistence:** Qdrant (Vector DB), PostgreSQL
- **Document Operations:** PyMuPDF, python-pptx, docx2txt, Pillow
- **Frontend Visualization:** Native Static HTML/CSS via FastAPI FileResponses.

## Project Structure

```text
├── airflow/           # Airflow DAGs, config, and modular plugins
├── api/               # FastAPI backend, static frontend templates, routing logic
├── app/               # Main execution modules, schemas, pipelines, and ML services
├── docker/            # Official Docker setups and containerized infrastructure
├── pyproject.toml     # Standard Python packaging, dependencies, constraints
└── requirements.txt   # Locked traditional requirements representation
```

## Setup & Prerequisites

Before continuing, you will need:
- Python 3.11+
- PostgreSQL Server
- Apache Airflow Installation (or utilize our Docker orchestration)
- Qdrant Vector Database
- Ollama Engine (with `minicpm-v` active)

### Getting Started

1. Clone and enter the repository.
2. Initialize dependencies strictly defined in `pyproject.toml` (e.g., using `uv` or `pip`).
3. Launch and coordinate essential infrastructure services (PostgreSQL, Qdrant, Airflow, Ollama).
4. Start docker containers using the command: docker compose -f docker/docker-compose.yaml up --build -d
5. Navigate securely to `http://localhost:8000` locally to engage the interface, securely upload documents, and interactively query your brand new knowledge engine.

---
**License**: Refer to the provided repository `LICENSE` file for usage details.
