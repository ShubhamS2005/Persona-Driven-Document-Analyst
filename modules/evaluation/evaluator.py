from modules.evaluation.retrieval_metrics import RetrievalEvaluator
from modules.evaluation.answer_metrics import PersonaEvaluator
from modules.evaluation.answer_metrics import ContextEvaluator



class RAGEvaluator:


    def __init__(self):

        self.retrieval=RetrievalEvaluator()

        self.persona=PersonaEvaluator()

        self.context=ContextEvaluator()



    def evaluate(
        self,
        result,
        expected
    ):


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