import os
import json
import pickle
import numpy as np


from modules.embeddings import EmbeddingModel



CHUNKS_PATH = "data/outputs/chunks.json"

VECTOR_FOLDER = "data/vector_store"

EMBEDDING_PATH = os.path.join(
    VECTOR_FOLDER,
    "embeddings.npy"
)


CHUNKS_PATH_OUTPUT = os.path.join(
    VECTOR_FOLDER,
    "chunks.pkl"
)



def load_chunks():

    with open(
        CHUNKS_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_embeddings(
    embeddings
):

    os.makedirs(
        VECTOR_FOLDER,
        exist_ok=True
    )


    np.save(
        EMBEDDING_PATH,
        embeddings
    )


def save_chunks(
    chunks
):

    with open(
        CHUNKS_PATH_OUTPUT,
        "wb"
    ) as f:

        pickle.dump(
            chunks,
            f
        )



def main():

    chunks = load_chunks()


    print(
        f"Loaded chunks: {len(chunks)}"
    )


    texts = [
        chunk["text"]
        for chunk in chunks
    ]


    model = EmbeddingModel()


    embeddings = model.generate_embeddings(
        texts
    )


    print(
        "\nEmbedding generated"
    )


    print(
        "Shape:",
        embeddings.shape
    )


    save_embeddings(
        embeddings
    )


    save_chunks(
        chunks
    )


    print(
        "\nSaved successfully"
    )

    print(
        EMBEDDING_PATH
    )

    print(
        CHUNKS_PATH_OUTPUT
    )



if __name__ == "__main__":
    main()