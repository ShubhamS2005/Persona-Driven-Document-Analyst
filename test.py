import json


with open(
"data/processed/processed_chunks.json"
) as f:

    chunks=json.load(f)


print("Total chunks:",len(chunks))


empty=[
c for c in chunks
if not c["text"].strip()
]


print("Empty chunks:",len(empty))


print(chunks[0])