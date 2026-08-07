# Backend Modules


## ingestion

Responsible for extracting information from PDFs.

Components:

- PyMuPDF extractor
- Docling extractor
- Document loader
- Document manager


Input:

PDF files


Output:

Structured documents



---

## processing

Responsible for cleaning and preparing documents.

Includes:

### Cleaner

Removes unnecessary noise.


### Metadata Enricher

Adds:

- document information
- page numbers
- source tracking


### Semantic Chunker

Creates meaningful chunks instead of fixed-length splits.



---

## embedding


Generates vector representations.

Model:

all-MiniLM-L6-v2


Output:

384 dimensional embeddings


Stored in:

data/vector_store/


---

## retrieval


Hybrid retrieval engine.


Components:


Dense Retriever

- FAISS similarity search


Keyword Retriever

- BM25 ranking


Hybrid Retriever

Combines both scores.



---

## persona


Determines the response personality.


Examples:

Research Analyst

Technical Expert

Summarizer


Based on:

- Query
- Retrieved context


---

## prompting


Creates optimized prompts for LLM generation.


---

## llm


Handles communication with language models.


---

## evaluation


Contains retrieval evaluation framework.


Measures:

- Retrieval accuracy
- Ranking quality
- Context relevance


---

## tests


Unit tests for individual components.
