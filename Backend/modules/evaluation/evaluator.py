class RAGEvaluator:
    def __init__(self):
        self.retrieval=RetrievalEvaluator()

        self.persona=PersonaEvaluator()

        self.context=ContextEvaluator()



    def evaluate(self,result,expected):
        report={}

        report["retrieval_hit"]=self.retrieval.hit_rate(
            result["retrieved"],
            expected["expected_sources"]
        )


        report["precision@3"]=self.retrieval.precision_at_k(
            result["retrieved"],
            expected["expected_sources"]
        )


        report["persona_accuracy"]=self.persona.check_persona(
            result["persona"]["persona"],
            expected["expected_persona"]
        )


        report["context_score"]=self.context.length_score(
            result["context"]
        )


        return report

class RetrievalEvaluator:
    def hit_rate(self,retrieved_chunks,expected_sources):
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



    def precision_at_k(self,retrieved_chunks,expected_sources,k=3):
        retrieved_chunks = retrieved_chunks[:k]
        correct=0
        for chunk in retrieved_chunks:
            title=chunk["metadata"]["section_title"]
            for expected in expected_sources:
                if expected.lower() in title.lower():
                    correct+=1
        return correct/k

class PersonaEvaluator:
    def check_persona(self,predicted,expected):
        return int(
            predicted==expected
        )

class ContextEvaluator:
    def length_score(self,context):
        words=len(context.split())

        if words < 100:
            return 0


        if words < 500:
            return 1


        return 2