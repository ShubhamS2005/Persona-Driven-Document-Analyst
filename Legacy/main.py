import os
import json
from datetime import datetime


from Legacy.modules.extractor import extract_outline, extract_section_blocks, extract_pages_text
from Legacy.modules.filters import refine_outline_structure
from Legacy.modules.relevence_model import compute_relevance_score
from Legacy.modules.rank_sections import rank_sections

# === Optional: Enable/Disable Phase 3 ===
RUN_PHASE_3 = True

COLLECTIONS_DIR = "input"

def ensure_directories():
    os.makedirs(COLLECTIONS_DIR, exist_ok=True)


def find_all_pdfs(root_dir):
    pdf_paths = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_paths.append(os.path.join(root, file))
    return pdf_paths

def process_pdfs(collection_path, input_documents):
    pdf_dir = os.path.join(collection_path, "PDFs")
    sections, subsection_analysis = [], []

    for doc in input_documents:
        pdf_path = os.path.join(pdf_dir, doc)
        if not os.path.exists(pdf_path):
            print(f"Missing PDF: {pdf_path}")
            continue

        base_name = os.path.splitext(doc)[0]
        print(f" Extracting from: {doc}")

        try:
            result = extract_outline(pdf_path)
            result["outline"] = refine_outline_structure(result.get("outline", []))
            page_texts = extract_pages_text(pdf_path)
            blocks = extract_section_blocks(base_name, result["outline"], page_texts)

            for block in blocks:
                sections.append(block)
                subsection_analysis.append({
                    "doc": block["doc"],
                    "page": block["page"],
                    "refined_text": block["body_text"]
                })

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f" Failed to process {doc}: {e}")
            continue

    return sections, subsection_analysis


def build_output_json(input_documents, persona, job, ranked_sections, subsection_analysis):
    return {
        "input_documents": input_documents,
        "persona": persona,
        "job_to_be_done": job,
        "ranked_sections": ranked_sections,
        "subsection_analysis": subsection_analysis
    }

def run_phase_3():

    for collection in sorted(os.listdir(COLLECTIONS_DIR)):
        collection_path = os.path.join(COLLECTIONS_DIR, collection)
        if not os.path.isdir(collection_path):
            continue

        print(f"\n Processing {collection}...")

        input_json_path = os.path.join(collection_path, "challenge1b_input.json")
        pdf_dir = os.path.join(collection_path, "pdfs")
        output_json_path = os.path.join(collection_path, "challenge1b_output.json")

        if not os.path.exists(input_json_path) or not os.path.exists(pdf_dir):
            continue

        with open(input_json_path, "r", encoding="utf-8") as f:
            input_data = json.load(f)

        persona = input_data.get("persona", {}).get("role", "")
        job = input_data.get("job_to_be_done", {}).get("task", "")
        query = f"{persona}: {job}"

        input_documents = [
            doc["filename"]
            for doc in input_data.get("documents", [])
            if isinstance(doc, dict) and "filename" in doc
        ]

        # 🔄 Process PDFs and extract relevant sections
        sections, subsection_analysis = process_pdfs(collection_path, input_documents)

        if not sections:
            continue

        scored_sections = compute_relevance_score(query, sections)
        ranked_sections = rank_sections(scored_sections)

        final_output = {
            "input_documents": input_documents,
            "persona": persona,
            "job_to_be_done": job,
            "ranked_sections": ranked_sections,
            "subsection_analysis": subsection_analysis,
            "processing_timestamp": datetime.now().isoformat(),
        }

        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)

        print(f"Output written to {output_json_path}")




if __name__ == "__main__":
    if RUN_PHASE_3:
        run_phase_3()
