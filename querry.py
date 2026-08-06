import os
import json
import gc


from modules.ingestion.document_loader import DocumentLoader

from modules.processing.cleaner import Cleaner
from modules.processing.structure_builder import StructureBuilder
from modules.processing.semantic_chunker import SemanticChunker
from modules.processing.metadata_enricher import MetadataEnricher


from modules.embedding.embedding_generator import EmbeddingGenerator
from modules.retrieval.vector_store import VectorStore



INPUT_DIR = "data/input_pdfs"


RAW_OUTPUT = "data/processed/raw_documents.json"

PROCESSED_OUTPUT = "data/processed/processed_chunks.json"




def phase_1():


    loader = DocumentLoader()

    all_documents = []


    for file in os.listdir(INPUT_DIR):

        if not file.lower().endswith(".pdf"):
            continue


        path=os.path.join(
            INPUT_DIR,
            file
        )


        print(
            "\nProcessing:",
            file
        )


        try:

            docs=loader.load(
                path
            )


            if not docs:

                print(
                    "No extraction:",
                    file
                )

                continue



            for d in docs:

                d["document"]=file



            all_documents.extend(
                docs
            )


            print(
                "Added:",
                len(docs),
                "elements"
            )


        except Exception as e:


            print(
                "Failed:",
                file,
                e
            )


        finally:

            gc.collect()



    os.makedirs(
        "data/processed",
        exist_ok=True
    )



    with open(
        RAW_OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            all_documents,
            f,
            indent=2,
            ensure_ascii=False
        )



    print(
        "\nSaved:",
        len(all_documents),
        "elements"
    )





def phase_2():


    print("\nPHASE 2 STARTED")


    with open(
        RAW_OUTPUT,
        encoding="utf-8"
    ) as f:


        elements=json.load(f)



    cleaner=Cleaner()


    elements=cleaner.clean_elements(
        elements
    )



    builder=StructureBuilder()


    sections=builder.build_sections(
        elements
    )



    chunker=SemanticChunker()


    chunks=chunker.create_chunks(
        sections
    )



    enricher=MetadataEnricher()


    chunks=enricher.enrich(
        chunks
    )



    os.makedirs(
        "data/processed",
        exist_ok=True
    )



    with open(
        PROCESSED_OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )



    print(
        "\nGenerated chunks:",
        len(chunks)
    )






def phase_3():


    print("\nPHASE 3 STARTED")


    with open(
        PROCESSED_OUTPUT,
        encoding="utf-8"
    ) as f:


        chunks=json.load(f)



    print(
        "Loaded chunks:",
        len(chunks)
    )



    texts=[

        chunk["text"]

        for chunk in chunks

    ]



    # -------------------------
    # Generate Embeddings
    # -------------------------

    generator=EmbeddingGenerator()



    embeddings=generator.generate_embeddings(
        texts
    )



    # -------------------------
    # Create Vector Store
    # -------------------------

    vector_store=VectorStore()



    index=vector_store.create_index(
        embeddings
    )



    vector_store.save(
        index,
        embeddings,
        chunks
    )



    print(
        "\nPhase 3 completed"
    )







if __name__=="__main__":


    # phase_1()
    
    # phase_2()

    phase_3()