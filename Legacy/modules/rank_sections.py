def rank_sections(scored_sections):
    """
    Takes a list of scored sections and returns cleaned, ranked sections
    for output JSON.
    """
    extracted_sections = []
    
    for rank, sec in enumerate(scored_sections, start=1):
        extracted_sections.append({
            "document": sec["doc"],
            "section_title": sec["section_title"],
            "importance_rank": rank,
            "page_number": sec["page"]
        })
    
    return extracted_sections
