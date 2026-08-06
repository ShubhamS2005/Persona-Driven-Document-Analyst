from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from modules.persona.persona import PersonaManager



class PersonaDetector:


    def __init__(self):

        self.manager = PersonaManager()


        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )


        self.personas = (
            self.manager.all_personas()
        )


        self.names=list(
            self.personas.keys()
        )


        profiles=[]


        for name in self.names:


            data=self.personas[name]


            text = (

                data["description"]
                +
                " "
                +
                " ".join(
                    data["keywords"]
                )

            )


            profiles.append(text)



        self.profile_embeddings = (
            self.model.encode(
                profiles
            )
        )



    def keyword_score(
        self,
        query,
        keywords
    ):


        query=query.lower()


        matches=0


        for word in keywords:


            if word.lower() in query:

                matches+=1



        if len(keywords)==0:

            return 0



        return matches / len(keywords)




    def detect(
        self,
        query
    ):


        query_embedding = self.model.encode(
            [query]
        )



        semantic_scores = cosine_similarity(

            query_embedding,

            self.profile_embeddings

        )[0]



        final_scores=[]


        for idx,name in enumerate(self.names):


            keyword=self.keyword_score(

                query,

                self.personas[name]["keywords"]

            )


            score=(

                0.6 * semantic_scores[idx]

                +

                0.4 * keyword

            )


            final_scores.append(score)




        best_index=max(
            range(len(final_scores)),
            key=lambda i: final_scores[i]
        )


        persona=self.names[
            best_index
        ]


        confidence = float(
    final_scores[best_index]
)


        return {

    "persona": persona,

    "confidence": float(confidence),

    "similarity_score": float(confidence),


    "details":
    self.personas[persona].get(
        "details",
        {}
    ),


    "all_scores":
    {
        name: float(score)
        for name, score in zip(
            self.names,
            final_scores
        )
    }
}