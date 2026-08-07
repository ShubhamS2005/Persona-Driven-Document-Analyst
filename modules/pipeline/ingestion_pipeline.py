import os

from modules.ingestion.document_loader import DocumentLoader

from modules.processing.cleaner import Cleaner
from modules.processing.structure_builder import StructureBuilder
from modules.processing.semantic_chunker import SemanticChunker
from modules.processing.metadata_enricher import MetadataEnricher

from modules.embedding.embedding_generator import EmbeddingGenerator

from modules.retrieval.vector_store import VectorStore



class IngestionPipeline:



    def __init__(self):


        self.loader = DocumentLoader()

        self.cleaner = Cleaner()

        self.structure_builder = StructureBuilder()

        self.chunker = SemanticChunker()

        self.metadata = MetadataEnricher()

        self.embedder = EmbeddingGenerator()

        self.vector_store = VectorStore()



    def ingest_pdf(
        self,
        pdf_path
    ):


        print(
            "\nINGESTING:",
            pdf_path
        )



        # --------------------------
        # STEP 1
        # Extract PDF
        # --------------------------

        elements = self.loader.load(
            pdf_path
        )


        if not elements:

            raise Exception(
                "PDF extraction failed"
            )



        filename = os.path.basename(
            pdf_path
        )



        for item in elements:

            item["document"] = filename



        print(
            "Extracted:",
            len(elements),
            "elements"
        )



        # --------------------------
        # STEP 2
        # Clean
        # --------------------------

        elements = self.cleaner.clean_elements(
            elements
        )



        # --------------------------
        # STEP 3
        # Build Structure
        # --------------------------

        sections = (
            self.structure_builder
            .build_sections(
                elements
            )
        )



        # --------------------------
        # STEP 4
        # Semantic Chunks
        # --------------------------

        chunks = (
            self.chunker.create_chunks(
                sections
            )
        )



        # --------------------------
        # STEP 5
        # Metadata
        # --------------------------

        chunks = self.metadata.enrich(
            chunks
        )


        print(
            "Generated chunks:",
            len(chunks)
        )



        # --------------------------
        # STEP 6
        # Generate Embeddings
        # --------------------------

        texts = [

            chunk["text"]

            for chunk in chunks

        ]


        embeddings = (
            self.embedder
            .generate_embeddings(
                texts
            )
        )



        # --------------------------
        # STEP 7
        # Incremental Vector Update
        # --------------------------

        self.vector_store.add_embeddings(
            embeddings,
            chunks
        )


        print(
            "Document ingestion completed"
        )


        return {

            "document":
            filename,

            "chunks":
            len(chunks)

        }