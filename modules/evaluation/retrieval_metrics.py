class RetrievalEvaluator:
    def hit_rate(
        self,
        retrieved_chunks,
        expected_sources
    ):


        retrieved_titles=[]


        for chunk in retrieved_chunks:

            retrieved_titles.append(
                chunk["metadata"]["section_title"]
            )


        for expected in expected_sources:

            for title in retrieved_titles:

                if expected.lower() in title.lower():

                    return 1


        return 0



    def precision_at_k(
        self,
        retrieved_chunks,
        expected_sources,
        k=3
    ):


        retrieved_chunks = retrieved_chunks[:k]


        correct=0


        for chunk in retrieved_chunks:


            title=chunk["metadata"]["section_title"]


            for expected in expected_sources:

                if expected.lower() in title.lower():

                    correct+=1


        return correct/k