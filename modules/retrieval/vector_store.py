import faiss
import numpy as np
import pickle
import os



class VectorStore:


    def __init__(
        self,
        path="data/vector_store"
    ):


        self.path = path


        self.index_path = os.path.join(
            self.path,
            "faiss.index"
        )


        self.embeddings_path = os.path.join(
            self.path,
            "embeddings.npy"
        )


        self.chunks_path = os.path.join(
            self.path,
            "chunks.pkl"
        )


        os.makedirs(
            self.path,
            exist_ok=True
        )



    # -----------------------------
    # CREATE FIRST INDEX
    # -----------------------------

    def create_index(
        self,
        embeddings
    ):


        dimension = embeddings.shape[1]


        index = faiss.IndexFlatIP(
            dimension
        )


        index.add(
            embeddings
        )


        print(
            "FAISS vectors:",
            index.ntotal
        )


        return index



    # -----------------------------
    # SAVE INITIAL STORE
    # -----------------------------

    def save(
        self,
        index,
        embeddings,
        chunks
    ):


        faiss.write_index(
            index,
            self.index_path
        )


        np.save(
            self.embeddings_path,
            embeddings
        )


        with open(
            self.chunks_path,
            "wb"
        ) as f:

            pickle.dump(
                chunks,
                f
            )


        print(
            "Vector store saved"
        )



    # -----------------------------
    # LOAD EXISTING STORE
    # -----------------------------

    def load(self):


        print(
            "Loading FAISS index..."
        )


        index = faiss.read_index(
            self.index_path
        )


        embeddings = np.load(
            self.embeddings_path
        )


        with open(
            self.chunks_path,
            "rb"
        ) as f:

            chunks = pickle.load(f)



        print(
            "Loaded:",
            index.ntotal,
            "vectors and",
            len(chunks),
            "chunks"
        )


        return (
            index,
            embeddings,
            chunks
        )



    # -----------------------------
    # INCREMENTAL VECTOR UPDATE
    # -----------------------------

    def add_embeddings(
        self,
        new_embeddings,
        new_chunks
    ):


        # Load existing data

        index, embeddings, chunks = self.load()



        # -------------------------
        # Add vectors to FAISS
        # -------------------------

        index.add(
            new_embeddings
        )



        # -------------------------
        # Update embeddings.npy
        # -------------------------

        updated_embeddings = np.vstack(
            [
                embeddings,
                new_embeddings
            ]
        )



        np.save(
            self.embeddings_path,
            updated_embeddings
        )



        # -------------------------
        # Update chunks.pkl
        # -------------------------

        chunks.extend(
            new_chunks
        )


        with open(
            self.chunks_path,
            "wb"
        ) as f:


            pickle.dump(
                chunks,
                f
            )



        # -------------------------
        # Save FAISS index
        # -------------------------

        faiss.write_index(
            index,
            self.index_path
        )



        print(
            "Incremental update complete"
        )


        print(
            "Total vectors:",
            index.ntotal
        )



        return index