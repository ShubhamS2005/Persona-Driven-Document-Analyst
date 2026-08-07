from sentence_transformers import SentenceTransformer
import numpy as np



class EmbeddingGenerator:
    def __init__(self,model_name="sentence-transformers/all-MiniLM-L6-v2"):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            model_name
        )

    def generate_embeddings(self,texts):
        print(
            f"Generating embeddings for {len(texts)} chunks..."
        )

        embeddings = self.model.encode(texts,batch_size=32,show_progress_bar=True,normalize_embeddings=True)

        embeddings=np.array(embeddings)

        print("Embedding shape:",embeddings.shape)


        return embeddings