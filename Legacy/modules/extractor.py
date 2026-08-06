import fitz
import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from nltk import pos_tag, word_tokenize
import nltk

import spacy
from collections import Counter
nlp = spacy.load("en_core_web_sm")

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

### UTILITIES ###

def is_bold(flags): return bool(flags & 2)

def is_repetitive(text):
    words = text.lower().split()
    return len(set(words)) <= 2 and len(words) > 1

def clean_ocr_artifacts(text):
    words = text.split()
    return ' '.join([w for i, w in enumerate(words) if i < 2 or w != words[i-1] or w != words[i-2]])

def collapse_repeats(text):
    return re.sub(r'(\b\w+\b)( \1\b)+', r'\1', text)

def fix_spacing(text):
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    text = re.sub(r'(?<=\d)(?=[A-Z])', ' ', text)
    text = re.sub(r'([A-Z]{2,})([A-Z][a-z])', r'\1 \2', text)
    return text

def detect_script(text):
    scripts = defaultdict(int)
    for char in text:
        if char.isalpha():
            name = unicodedata.name(char, "")
            if "LATIN" in name: scripts["Latin"] += 1
            elif "CYRILLIC" in name: scripts["Cyrillic"] += 1
            elif "CJK" in name or "HIRAGANA" in name: scripts["Japanese"] += 1
            elif "HANGUL" in name: scripts["Korean"] += 1
            elif "ARABIC" in name: scripts["Arabic"] += 1
            elif "DEVANAGARI" in name: scripts["Devanagari"] += 1
    return max(scripts, key=scripts.get) if scripts else "Unknown"

def is_likely_instruction_or_ingredient(text, tokens, tags):
    """Reject headings that sound like ingredient instructions or measurements"""
    text_lower = text.lower()
    
    # Common culinary noise starters
    skip_starts = [
        "pinch of", "salt and pepper", "toppings:", "instructions:", "optional:", "preheat", 
        "add ", "bake ", "stir ", "pour ", "serve", "combine", "drizzle", "cook"
    ]
    if any(text_lower.startswith(phrase) for phrase in skip_starts):
        return True

    # Likely an ingredient line if it has too many numbers and units
    if re.search(r"\d+/?\d*\s?(cups?|tablespoons?|tbsp|tsp|grams?|oz|ml|liters?)", text_lower):
        return True

    # Overly short and lacks noun tags (not informative heading)
    noun_tags = [tag for _, tag in tags if tag.startswith('NN')]
    if len(tokens) < 4 and len(noun_tags) < 2:
        return True

    return False


def merge_spans_to_lines(blocks):
    lines = []
    for b in blocks:
        for line in b.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            spans = sorted(spans, key=lambda s: s["bbox"][0])
            text, sizes, flags, prev_x1 = "", [], [], None
            for span in spans:
                if not span["text"].strip():
                    continue
                x0 = span["bbox"][0]
                if prev_x1 is not None and (x0 - prev_x1 > 2):
                    text += " "
                text += span["text"].strip()
                sizes.append(span["size"])
                flags.append(span["flags"])
                prev_x1 = span["bbox"][2]
            lines.append({"text": text.strip(), "sizes": sizes, "flags": flags, "y0": line["bbox"][1]})
    return lines

def group_multiline_headings(lines):
    grouped, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line["sizes"]:
            i += 1
            continue

        text, sizes, flags = line["text"], line["sizes"][:], line["flags"][:]
        j = i + 1
        while j < len(lines):
            next_line = lines[j]
            if not next_line["sizes"] or not line["sizes"]:
                break
            ygap = next_line["y0"] - lines[j - 1]["y0"]
            avg_size_current = sum(line["sizes"]) / len(line["sizes"])
            avg_size_next = sum(next_line["sizes"]) / len(next_line["sizes"])
            size_diff = abs(avg_size_next - avg_size_current)

            if ygap < 20 and size_diff < 1.5 and not text.endswith(('.', ':')) and len(next_line["text"].split()) <= 6:
                text += " " + next_line["text"]
                sizes += next_line["sizes"]
                flags += next_line["flags"]
                j += 1
            else:
                break

        grouped.append({"text": text.strip(), "sizes": sizes, "flags": flags, "y0": line["y0"]})
        i = j
    return grouped

### MAIN OUTLINE EXTRACTOR ###

def extract_outline(pdf_path):
    print(f"\n Extracting from: {pdf_path}")
    doc = fitz.open(pdf_path)
    candidate_headings, possible_titles = [], []
    font_sizes_by_freq = defaultdict(int)
    base_font_size = 12

    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        lines = group_multiline_headings(merge_spans_to_lines(blocks))

        for line in lines:
            raw_text = line["text"]
            if not line["sizes"]:
                continue

            text = fix_spacing(clean_ocr_artifacts(collapse_repeats(raw_text))).strip()
            if len(text) < 3 or is_repetitive(text):
                continue

            avg_size = sum(line["sizes"]) / len(line["sizes"])
            if avg_size == 0:
                continue

            bold = any(is_bold(f) for f in line["flags"])
            tokens = word_tokenize(text)
            if not tokens:
                continue
            tags = pos_tag(tokens)
            y0 = line["y0"]

            # ❌ Filter bad candidates
            if len(tokens) < 3 and not bold and avg_size < 12:
                continue
            if text.endswith('.') and 3 <= len(tokens) <= 6:
                continue
            if any(tag.startswith("VBG") for _, tag in tags):  # e.g. 'Cooking', 'Traveling'
                continue
            if text[0].islower():
                continue
            if len(tokens) > 14:  # too long to be a heading
                continue
            if re.match(r".*:[^\s]", text):  # tips like "Make a Packing List:Bring a pen"
                continue
            if is_likely_instruction_or_ingredient(text, tokens, tags):
                continue

            font_sizes_by_freq[round(avg_size)] += 1
            valid_sizes = [(k, v) for k, v in font_sizes_by_freq.items() if k > 0]
            base_font_size = max(valid_sizes, key=lambda x: x[1])[0] if valid_sizes else 12

            cap_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
            script = detect_script(text)
            script_bonus = 3 if script != "Latin" else 0

            # ✅ Improved scoring
            score = avg_size + (4 * cap_ratio) + (5 if bold else 0) + script_bonus
            if y0 < 300: score += 3
            if len(tokens) <= 10: score += 2
            if text.endswith(":"): score += 2
            if text.istitle(): score += 1

            candidate_headings.append({
                "text": text,
                "page": page_number,
                "size": avg_size,
                "bold": bold,
                "y0": y0,
                "score": score
            })

            # Capture potential document title
            if page_number == 1 and y0 < page.rect.height * 0.2 and len(tokens) <= 10:
                possible_titles.append((score, text))

    outline = []
    used_texts = set()
    page_heading_count = defaultdict(int)

    for h in sorted(candidate_headings, key=lambda x: (-x["score"], -x["size"])):
        if h["text"] in used_texts or page_heading_count[h["page"]] >= 5:
            continue

        size, score = h["size"], h["score"]
        font_ratio = size / base_font_size if base_font_size else 1

        if score >= 16 and font_ratio >= 1.4:
            level = "H1"
        elif score >= 12 and font_ratio >= 1.2:
            level = "H2"
        elif score >= 9 and font_ratio >= 1.0:
            level = "H3"
        else:
            continue

        used_texts.add(h["text"])
        outline.append({
            "level": level,
            "text": h["text"],
            "page": h["page"] - 1
        })
        page_heading_count[h["page"]] += 1

    # Fallback if nothing is extracted
    if not outline:
        fallback = sorted(candidate_headings, key=lambda x: (-x["size"], x["page"]))
        for h in fallback[:5]:
            outline.append({"level": "H3", "text": h["text"], "page": h["page"] - 1})

    # Determine title
    title = (
        max(possible_titles, key=lambda x: x[0])[1]
        if possible_titles else
        next((h["text"] for h in outline if h["level"] == "H1"), outline[0]["text"] if outline else "UNKNOWN")
    )

    return {"title": title, "outline": outline}

### OUTLINE FILTER (PHASE 1 POST-PROCESSING) ###

def refine_outline_structure(outlines):
    def score(text):
        score = 0
        words = text.strip().split()
        wc, cc = len(words), len(text)
        if wc < 2 or cc < 10: score += 2
        if text.islower() and wc > 6: score += 1
        if text.isupper() and wc > 4: score += 1
        if re.search(r"^\d+(\.|\))?\s?", text): score += 2
        if re.search(r"\b\d+/?\d*\s?(cups?|tablespoons?|tbsp|tsp|grams?|oz|ml|liters?)\b", text, re.IGNORECASE): score += 2
        if sum(c.isdigit() for c in text) / (sum(c.isalpha() for c in text) or 1) > 0.3: score += 1
        if re.match(r"^[•\-\*\u2022]+\s", text): score += 1
        if text.count(",") >= 3 and ":" not in text: score += 1
        if wc > 25 and ":" not in text: score += 2
        if text.endswith(".") and ":" not in text: score += 1
        if re.match(r"^(Add|Pour|Top|Stir|Crack|Serve|Preheat|Place|Spread|Press|Heat|Combine|"
                    r"Bake|Mix|Whisk|Cook|Boil|Grease|Remove|Slice|Chop|Set|Let|Transfer|Layer|Use|Keep|Bring)\b", text, re.IGNORECASE): score += 2
        if re.match(r"^[A-Z][a-z]+\s(and|or)?\s?(pepper|salt|oil|egg|onion|cheese|spinach|bread|fruit|honey)\b", text, re.IGNORECASE):
            if wc < 5: score += 2
        return score

    seen, clean = set(), []
    for item in outlines:
        t = item["text"].strip()
        if t not in seen and score(t) == 0:
            clean.append(item)
            seen.add(t)
    return clean

### PHASE 2: BLOCK EXTRACTION with FUZZY MATCHING ###

def token_overlap_ratio(a, b):
    set_a = set(a.lower().split())
    set_b = set(b.lower().split())
    if not set_a or not set_b:
        return 0
    return len(set_a & set_b) / len(set_a | set_b)

def extract_section_blocks(doc_name, outlines, page_texts):
    blocks = []

    for outline in outlines:
        title, page_num = outline["text"], outline["page"]
        if page_num >= len(page_texts):
            continue

        lines = page_texts[page_num].split('\n')
        best_idx, best_score = -1, 0

        for idx in range(len(lines)):
            line = lines[idx].strip()
            next_line = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
            combined = f"{line} {next_line}".strip()

            fuzzy = SequenceMatcher(None, title.lower(), combined.lower()).ratio()
            token = token_overlap_ratio(title, combined)
            hybrid_score = 0.6 * fuzzy + 0.4 * token

            if hybrid_score > best_score:
                best_score = hybrid_score
                best_idx = idx

        # Confidence threshold to suppress noisy matches
        if best_score < 0.68:
            continue

        # Extract top 2 paragraphs after the heading
        remaining = "\n".join(lines[best_idx + 1:]).strip()
        paragraphs = re.split(r'\n{2,}', remaining)
        body = " ".join(paragraphs[:2]).strip()

        # Heuristic filter: avoid storing almost-empty or bullet-only blocks
        if not body or body.count("•") > 3 or len(body.split()) < 25:
            continue

        blocks.append(enrich_block_with_nlp({
            "doc": doc_name,
            "page": page_num,
            "section_title": title,
            "body_text": body
        }))

    return blocks


### PAGE TEXT EXTRACTOR ###

def extract_pages_text(doc_path):
    return [page.get_text() for page in fitz.open(doc_path)]

def enrich_block_with_nlp(block):
    doc = nlp(block["body_text"])

    # 1. Named Entities
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    # 2. Keyword Extraction (noun phrases + filtered nouns)
    noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
    filtered_nouns = [token.lemma_ for token in doc if token.pos_ == "NOUN" and not token.is_stop and len(token.text) > 2]
    
    keywords = [word for word, count in Counter(noun_chunks + filtered_nouns).most_common(10)]

    block["entities"] = entities
    block["keywords"] = keywords
    return block
