from modules.persona.persona_detector import PersonaDetector

from modules.retrieval.retriever import Retriever

from modules.retrieval.context_builder import ContextBuilder

from modules.prompting.prompt_builder import PromptBuilder




query="What are the historical sites in Carcassonne?"



# Persona

persona_detector=PersonaDetector()


persona=persona_detector.detect(
    query
)



print("\nPERSONA RESULT")
print(persona)



# Retrieval

retriever=Retriever()


chunks=retriever.search(
    query,
    top_k=3
)



print(
    "\nRetrieved:",
    len(chunks)
)



# Context

context_builder=ContextBuilder()


context=context_builder.build(

    chunks,

    persona

)



print(
    "\nFINAL CONTEXT"
)

print(context)



# Prompt

prompt_builder=PromptBuilder()


prompt=prompt_builder.build(

    query,

    context,

    persona

)



print(
    "\nFINAL PROMPT"
)


print(prompt)