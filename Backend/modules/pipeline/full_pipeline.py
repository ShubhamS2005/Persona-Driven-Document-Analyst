from modules.retrieval.retriever import Retriever
from modules.retrieval.context_builder import ContextBuilder

from modules.persona.persona_detector import PersonaDetector

from modules.prompting.prompt_builder import PromptBuilder

from modules.llm.llm_client import LLMClient
from modules.persona.persona import PersonaManager


class FullRAGPipeline:


    def __init__(
        self,
        retriever=None
    ):


        print("Initializing RAG Pipeline...")


        # ==========================
        # Shared Retriever Instance
        # ==========================

        if retriever is not None:

            self.retriever = retriever

            print(
                "Using shared Retriever"
            )

        else:

            self.retriever = Retriever()

            print(
                "Created new Retriever"
            )



        self.persona_detector = PersonaDetector()
        self.persona_manager = PersonaManager()

        self.context_builder = ContextBuilder()


        self.prompt_builder = PromptBuilder()


        self.llm = LLMClient()



        print("Pipeline Ready")



    def run(
        self,
        query,
        top_k=3
    ):


        print("\nUSER QUERY:")
        print(query)



        # ----------------------
        # Retrieval
        # ----------------------

        results = self.retriever.search(
            query,
            top_k
        )


        persona = self.persona_detector.detect(
            query,
            results

        )


        print("\nPERSONA:")
        print(
            persona["persona"]
        )



        # ----------------------
        # Context Building
        # ----------------------

        context = self.context_builder.build(
            results,
            persona
        )



        # ----------------------
        # Prompt
        # ----------------------

        prompt = self.prompt_builder.build(

            query,

            context,

            persona

        )



        # ----------------------
        # LLM
        # ----------------------

        answer = self.llm.generate(
            prompt
        )


        return {

            "query":query,

            "retrieved":results,

            "persona":persona,

            "context":context,

            "prompt":prompt,

            "answer":answer

        }
    