import os
import json
import gc

from modules.ingestion.document_loader import DocumentLoader

from modules.processing.cleaner import Cleaner
from modules.processing.structure_builder import StructureBuilder
from modules.processing.semantic_chunker import SemanticChunker
from modules.processing.metadata_enricher import MetadataEnricher

INPUT_DIR = "data/input_pdfs"

OUTPUT = "data/processed/raw_documents.json"

P_OUTPUT="data/processed/processed_chunks.json"


def phase_1():

    loader = DocumentLoader()

    all_documents = []


    for file in os.listdir(INPUT_DIR):

        if not file.lower().endswith(".pdf"):
            continue


        path = os.path.join(
            INPUT_DIR,
            file
        )


        print("\nProcessing:", file)


        try:

            docs = loader.load(path)


            if not docs:

                print(
                    f"No data extracted from {file}"
                )

                continue


            for d in docs:

                d["document"] = file


            all_documents.extend(
                docs
            )


            print(
                f"Added {len(docs)} elements"
            )


        except Exception as e:

            print(
                f"Failed processing {file}: {e}"
            )


        finally:

            # release memory after every PDF
            gc.collect()



    os.makedirs(
        "data/processed",
        exist_ok=True
    )


    with open(
        OUTPUT,
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


    with open(
        OUTPUT,
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



    with open(
        P_OUTPUT,
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
        "Generated chunks:",
        len(chunks)
    )


if __name__ == "__main__":

    # phase_1()
    phase_2()