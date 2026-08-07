from sentence_transformers import SentenceTransformer


class DocumentPersonaBuilder:


    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )



    def build(
        self,
        chunks
    ):


        if not chunks:

            return {

                "persona_profile":"",
                "embedding":[]

            }



        text = " ".join(

            [
                chunk["text"]

                for chunk in chunks[:10]

            ]

        )



        persona_profile = f"""

Analyze this document.

Document content:

{text}


Identify:

- domain
- expertise level
- possible user intent
- answer style

"""



        embedding = self.model.encode(
            persona_profile,
            normalize_embeddings=True
        )



        return {


            "persona_profile":
            persona_profile,


            "embedding":
            embedding.tolist()

        }