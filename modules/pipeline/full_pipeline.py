from modules.retrieval.retriever import Retriever
from modules.retrieval.context_builder import ContextBuilder

from modules.persona.persona_detector import PersonaDetector

from modules.prompting.prompt_builder import PromptBuilder

from modules.llm.llm_client import LLMClient



class FullRAGPipeline:


    def __init__(self):


        print("Initializing RAG Pipeline...")


        self.retriever = Retriever()


        self.persona_detector = PersonaDetector()


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
        # Persona Detection
        # ----------------------

        persona = self.persona_detector.detect(
            query
        )


        print("\nPERSONA:")
        print(
            persona["persona"]
        )



        # ----------------------
        # Retrieval
        # ----------------------

        results = self.retriever.search(
            query,
            top_k
        )


        print(
            "\nRetrieved:",
            len(results)
        )



        # ----------------------
        # Context Building
        # ----------------------

        context = self.context_builder.build(
            results,
            persona
        )



        # ----------------------
        # Prompt Creation
        # ----------------------

        prompt = self.prompt_builder.build(

        query,
    
        context,
    
        persona
    
    )



        # ----------------------
        # LLM Generation
        # ----------------------

        answer = self.llm.generate(
            prompt
        )



        return {

    "query": query,

    "retrieved": results,

    "persona": persona,

    "context": context,

    "prompt": prompt,

    "answer": answer
}