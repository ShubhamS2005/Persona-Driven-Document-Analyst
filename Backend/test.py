import pickle

with open(
    "data/vector_store/chunks.pkl",
    "rb"
) as f:

    chunks = pickle.load(f)


print(len(chunks))

for c in chunks[:5]:
    print(
        c["metadata"]["document"]
    )