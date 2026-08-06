import re
from typing import List, Dict

def refine_outline_structure(outlines: List[Dict]) -> List[Dict]:
    def calculate_heading_score(text: str) -> int:
        score = 0
        text = text.strip()
        words = text.split()
        word_count = len(words)
        char_count = len(text)

        # Rule 1: Too short (not informative)
        if word_count < 2 or char_count < 10:
            score += 2

        # Rule 2: Suspicious casing and long text
        if text.islower() and word_count > 6:
            score += 1
        if text.isupper() and word_count > 4:
            score += 1

        # Rule 3: Starts with number or quantity unit — usually instructions or ingredients
        if re.search(r"^\d+(\.|\))?\s?", text):  # "1. Step..."
            score += 2
        if re.search(r"\b\d+/?\d*\s?(cups?|tablespoons?|tbsp|tsp|grams?|oz|ml|liters?)\b", text, re.IGNORECASE):
            score += 2

        # Rule 4: High digit density — indicative of recipe content
        digits = sum(c.isdigit() for c in text)
        letters = sum(c.isalpha() for c in text)
        if letters > 0 and digits / letters > 0.3:
            score += 1

        # Rule 5: Bullet or list markers
        if re.match(r"^[•\-\*\u2022]+\s", text):
            score += 1

        # Rule 6: Too many commas but no structure (no colon)
        if text.count(",") >= 3 and ":" not in text:
            score += 1

        # Rule 7: Very long line without structural indicator (like ':')
        if word_count > 25 and ":" not in text:
            score += 2

        # Rule 8: Ends with a period but no colon — likely a sentence
        if text.endswith(".") and ":" not in text:
            score += 1

        # Rule 9: Starts with imperative/instructional verb (typical in recipes, guides)
        if re.match(r"^(Add|Pour|Top|Stir|Crack|Serve|Preheat|Place|Spread|Press|Heat|Combine|"
                    r"Bake|Mix|Whisk|Cook|Boil|Grease|Remove|Slice|Chop|Set|Let|Transfer|Layer|Use|Keep|Bring)\b", text, re.IGNORECASE):
            score += 2

        # Rule 10: Generic short ingredient phrases (likely not headings)
        if re.match(r"^[A-Z][a-z]+\s(and|or)?\s?(pepper|salt|oil|egg|onion|cheese|spinach|bread|fruit|honey)\b", text, re.IGNORECASE):
            if word_count < 5:
                score += 2

        return score

    filtered_outlines = []
    seen_texts = set()

    for item in outlines:
        clean_text = item["text"].strip()

        # Final strict filter: score must be 0 (perfectly clean)
        if clean_text not in seen_texts and calculate_heading_score(clean_text) == 0:
            filtered_outlines.append(item)
            seen_texts.add(clean_text)

    return filtered_outlines
