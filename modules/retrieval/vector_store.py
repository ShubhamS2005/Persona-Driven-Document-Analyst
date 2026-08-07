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

        if not os.path.exists(self.index_path):
        
            print(
                "Vector store not found. Starting empty."
            )
    
            return (
                None,
                np.array([]),
                []
            )
    
    
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


        # -----------------------------
        # FIRST DOCUMENT
        # -----------------------------

        if not os.path.exists(self.index_path):


            print(
                "Creating first vector store..."
            )


            index = self.create_index(
                new_embeddings
            )


            self.save(
                index,
                new_embeddings,
                new_chunks
            )


            return index



        # -----------------------------
        # EXISTING STORE
        # -----------------------------


        index, embeddings, chunks = self.load()



        print(
            "Existing chunks:",
            len(chunks)
        )


        print(
            "Adding new chunks:",
            len(new_chunks)
        )



        # Add vectors

        index.add(
            new_embeddings
        )



        # Merge embeddings

        updated_embeddings = np.vstack(
            [
                embeddings,
                new_embeddings
            ]
        )



        # Merge metadata

        chunks.extend(
            new_chunks
        )



        self.save(
            index,
            updated_embeddings,
            chunks
        )


        print(
            "Incremental update complete"
        )


        print(
            "Total vectors:",
            index.ntotal
        )


        return index

    def remove_document(self,document_name):

        index, embeddings, chunks = self.load()


        filtered_chunks = []
        filtered_embeddings = []



        for emb, chunk in zip(
            embeddings,
            chunks
        ):


            if chunk["metadata"].get("document") != document_name:

                filtered_chunks.append(
                    chunk
                )

                filtered_embeddings.append(
                    emb
                )



        if len(filtered_chunks)==0:

            print(
                "No vectors remaining"
            )

            return



        filtered_embeddings = np.array(
            filtered_embeddings
        ).astype(
            "float32"
        )



        new_index = self.create_index(
            filtered_embeddings
        )



        self.save(
            new_index,
            filtered_embeddings,
            filtered_chunks
        )


        print(
            "Vector cleanup completed:",
            document_name
        )