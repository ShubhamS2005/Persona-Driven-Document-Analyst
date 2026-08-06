from sentence_transformers import SentenceTransformer, util
import torch
from Legacy.modules.rank_sections import rank_sections
# Load the model (make sure to download in advance and cache for offline use)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def compute_relevance_score(query, sections):
    """
    query: str (Persona + job-to-be-done)
    sections: list of dicts with keys: {'text': str, 'title': str, 'doc': str, 'page': int}
    
    Returns: list of dicts with added key 'score'
    """
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    for section in sections:
        section_text = section['body_text']
        section_embedding = model.encode(section_text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(query_embedding, section_embedding).item()
        section['score'] = round(similarity, 4)
    
    # Sort by descending score
    sorted_sections = sorted(sections, key=lambda x: x['score'], reverse=True)
    
    return sorted_sections




