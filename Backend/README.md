# Backend Architecture

The backend contains the complete AI pipeline powering Persona RAG.

## Responsibilities

- PDF ingestion
- Document processing
- Semantic chunking
- Embedding generation
- Hybrid retrieval
- Persona detection
- LLM response generation
- Evaluation


## Backend Flow


PDF Upload

↓

Ingestion Pipeline

↓

Document Processing

↓

Semantic Chunking

↓

Embedding Generation

↓

FAISS + BM25 Retrieval

↓

Persona Engine

↓

LLM Response


## Folder Structure

Backend/

├── api/
│   REST endpoints

├── modules/

│
├── data/
│
└── app.py

