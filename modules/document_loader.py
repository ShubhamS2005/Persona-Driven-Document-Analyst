import os
def find_all_pdfs(root_dir):
    pdf_paths = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_paths.append(os.path.join(root, file))
    return pdf_paths