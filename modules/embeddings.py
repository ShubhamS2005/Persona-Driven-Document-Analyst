from sentence_transformers import SentenceTransformer
import numpy as np


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingModel:

    def __init__(self):

        print(
            "Loading embedding model..."
        )

        self.model = SentenceTransformer(
            MODEL_NAME
        )


    def generate_embeddings(self, texts):

        print(
            f"Generating embeddings for {len(texts)} chunks..."
        )


        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )


        return embeddings