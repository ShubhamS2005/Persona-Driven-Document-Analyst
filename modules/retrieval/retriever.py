from modules.retrieval.hybrid_retriever import HybridRetriever



class Retriever:
    def __init__(self):
        print("Initializing Retriever...")
        self.retriever = HybridRetriever()

    def search(self,query,top_k=5):
        results = self.retriever.retrieve(
            query,
            top_k
        )

        return results