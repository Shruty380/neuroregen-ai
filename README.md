# NeuroRegen AI

> An AI-powered bioinformatics platform for neurodegenerative disease research and regenerative biology.

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Quick Start (Docker)

```bash
git clone https://github.com/Shruty380/neuroregen-ai.git
cd neuroregen-ai
docker-compose up
```

Visit:
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Dashboard: http://localhost:3000/dashboard

---

## Platform Overview

NeuroRegen AI combines bioinformatics, machine learning, and a curated disease knowledge base to study neurodegenerative diseases.

### Core Features

| Feature | Description |
|---------|-------------|
| Disease Knowledge Base | Structured data for Alzheimer's, Parkinson's, ALS, Huntington's |
| Gene Database | Associated genes with chromosomal locations and risk levels |
| Biomarker Tracking | Clinical biomarkers with sample sources and significance |
| NCBI Integration | Live gene and protein data from NCBI databases |
| AI Disease Classifier | Random Forest model predicting disease from biomarker profiles |
| Explainable AI | Feature importance scores for every prediction |
| PDF Report Generator | Downloadable research reports per disease |
| CSV Export | Bioinformatics-standard data export |
| Research Dashboard | Interactive frontend connecting all platform features |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, React, TailwindCSS |
| Backend | FastAPI, Python 3.9 |
| Database | SQLite (dev), PostgreSQL (prod) |
| AI/ML | scikit-learn, Random Forest |
| Bioinformatics | Biopython, NCBI Entrez API |
| DevOps | Docker, Docker Compose |

---

## API Endpoints

### Diseases
- `GET /diseases/` — All diseases with genes and biomarkers
- `GET /diseases/{id}` — Single disease
- `GET /diseases/{id}/genes` — Disease genes
- `GET /diseases/{id}/biomarkers` — Disease biomarkers

### Bioinformatics
- `GET /bio/gene/{symbol}` — Fetch gene from NCBI
- `GET /bio/protein/{id}` — Fetch protein sequence
- `GET /bio/pubmed/{query}` — Search PubMed papers
- `POST /bio/analyze` — Analyze DNA/protein sequence
- `POST /bio/blast` — BLAST sequence search

### AI Models
- `POST /ai/predict/disease` — Predict disease from biomarkers
- `GET /ai/demo/alzheimers` — Alzheimer's demo prediction
- `GET /ai/demo/parkinsons` — Parkinson's demo prediction
- `GET /ai/model/info` — Model architecture and accuracy

### Export
- `GET /export/disease/{id}/pdf` — Download PDF report
- `GET /export/diseases/csv` — Download CSV dataset
- `GET /export/methods` — Research methods section

---

## Manual Setup (without Docker)

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 seed_data.py
python3 -m uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## Scientific Background

This platform studies four major neurodegenerative diseases:

**Alzheimer's Disease** — Progressive memory loss from amyloid-beta plaques and tau tangles. Key genes: APOE4, APP, PSEN1.

**Parkinson's Disease** — Loss of dopaminergic neurons in the substantia nigra. Key genes: SNCA, LRRK2, PINK1.

**ALS** — Motor neuron degeneration causing paralysis. Key genes: SOD1, C9orf72, FUS.

**Huntington's Disease** — CAG repeat expansion producing toxic huntingtin protein. Key gene: HTT.

---

## AI Model

- Algorithm: Random Forest Classifier (100 trees)
- Features: 10 biomarkers including amyloid-beta, phospho-tau, neurofilament light chain
- Training: Synthetic data following known biological patterns
- Accuracy: 100% on test set
- Explainability: Feature importance from ensemble

---

## Research Question

Can AI accelerate the discovery of therapeutic targets for neurodegenerative diseases by analyzing patterns in multi-modal biomarker data?

---

## Author

Built by Shruty — Biotechnology graduate exploring the intersection of AI and computational biology.

**github.com/Shruty380** · **shruty1522@gmail.com**