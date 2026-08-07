from modules.pipeline.ingestion_pipeline import IngestionPipeline
from modules.retrieval.vector_store import VectorStore
from modules.retrieval.retriever import Retriever
from modules.ingestion.document_manager import DocumentManager

import os


PDF_FOLDER = "data/demo_documents"


print("Building Demo Knowledge Base...")


ingestion = IngestionPipeline()

vector_store = VectorStore()

document_manager = DocumentManager()


for file in os.listdir(PDF_FOLDER):

    if file.endswith(".pdf"):

        path = os.path.join(
            PDF_FOLDER,
            file
        )

        print("Processing:", file)


        result = ingestion.ingest_pdf(path)


        document_manager.add(
            result["document"],
            result["chunks"],
            result.get("persona")
        )


print("Refreshing vector database")

retriever = Retriever()

retriever.refresh()


print("Demo Index Created Successfully")