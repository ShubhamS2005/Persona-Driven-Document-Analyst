from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



class PersonaDetector:


    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )



    def detect(
        self,
        query,
        retrieved_chunks,
        document_persona=None
    ):


        if not retrieved_chunks:

            return {

                "persona":
                "general assistant",

                "confidence":
                0.0

            }



        context = " ".join(

            [
                chunk["text"]

                for chunk in retrieved_chunks

            ]

        )



        combined = f"""

Question:

{query}


Document evidence:

{context}

"""



        query_embedding = self.model.encode(
            combined,
            normalize_embeddings=True
        )



        confidence = 0.5



        # Compare with uploaded document identity

        if document_persona and document_persona.get("embedding"):


            persona_embedding = (
                document_persona["embedding"]
            )


            similarity = cosine_similarity(

                [
                    query_embedding
                ],

                [
                    persona_embedding
                ]

            )[0][0]


            confidence = float(similarity)



        persona = self.classify(

            query,

            context

        )



        return {


            "persona":
            persona,


            "confidence":
            confidence


        }



    def classify(
        self,
        query,
        context
    ):


        text = (

            query
            +
            " "
            +
            context

        ).lower()



        scores = {


            "technical mentor":[

                "python",
                "code",
                "software",
                "machine learning",
                "model",
                "algorithm"

            ],



            "career advisor":[

                "resume",
                "experience",
                "skills",
                "project",
                "internship",
                "education"

            ],



            "research analyst":[

                "research",
                "paper",
                "experiment",
                "analysis",
                "dataset"

            ],



            "historical analyst":[

                "history",
                "century",
                "empire",
                "war",
                "culture"

            ],



            "travel advisor":[

                "travel",
                "visit",
                "hotel",
                "place",
                "restaurant"

            ]

        }



        best = "general assistant"

        max_score = 0



        for persona, keywords in scores.items():


            score=sum(

                1

                for word in keywords

                if word in text

            )



            if score > max_score:

                max_score = score

                best = persona



        return best