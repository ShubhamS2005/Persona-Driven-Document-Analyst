import os
import json

from modules.extractor import (
    extract_outline,
    extract_section_blocks,
    extract_pages_text
)

from modules.filters import (
    refine_outline_structure
)

from modules.chunker import (
    create_chunks
)



PDF_FOLDER = "data/input_pdfs"

OUTPUT_FOLDER = "data/outputs"



def find_pdfs(folder):

    pdfs = []

    for file in os.listdir(folder):

        if file.lower().endswith(".pdf"):

            pdfs.append(
                os.path.join(folder,file)
            )

    return pdfs



def process_documents():


    all_sections = []


    pdf_files = find_pdfs(
        PDF_FOLDER
    )


    for pdf_path in pdf_files:


        doc_name = os.path.splitext(
            os.path.basename(pdf_path)
        )[0]


        print(
            f"\nProcessing {doc_name}"
        )


        outline_result = extract_outline(
            pdf_path
        )


        outline = refine_outline_structure(
            outline_result["outline"]
        )


        pages = extract_pages_text(
            pdf_path
        )


        sections = extract_section_blocks(
            doc_name,
            outline,
            pages
        )


        print(
            f"Sections extracted: {len(sections)}"
        )


        all_sections.extend(
            sections
        )



    print(
        "\nCreating chunks..."
    )


    chunks = create_chunks(
        all_sections
    )


    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )


    output_path = os.path.join(
        OUTPUT_FOLDER,
        "chunks.json"
    )


    with open(
        output_path,
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
        f"\nSaved {len(chunks)} chunks"
    )

    print(
        output_path
    )



if __name__ == "__main__":

    process_documents()