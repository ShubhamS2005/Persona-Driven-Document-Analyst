from datetime import datetime

def build_output_json(input_docs, persona, job_to_be_done, extracted_sections, subsection_analysis):
    output = {
        "metadata": {
            "input_documents": input_docs,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }
    return output
