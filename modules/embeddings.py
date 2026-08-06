from sentence_transformers import SentenceTransformer
import torch



MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"



class EmbeddingModel:


    def __init__(self):

        print(
            "Loading embedding model..."
        )


        self.model = SentenceTransformer(
            MODEL_NAME,
            device="cpu"
        )


    def generate_embeddings(
        self,
        texts
    ):


        embeddings = self.model.encode(
            texts,
            batch_size=16,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )


        return embeddings



    def encode_query(
        self,
        query
    ):


        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )


        return embedding.astype(
            "float32"
        )