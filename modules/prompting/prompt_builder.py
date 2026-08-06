class PromptBuilder:
    def build(self,query,context,persona):


        prompt = f"""
You are an AI assistant answering as a:

PERSONA:
{persona['persona']}


ANSWER STYLE:
{persona['details']['style']}


YOUR ROLE:

Answer the user's question from the perspective of the selected persona.


GROUNDING RULES:

- Use only the provided document evidence.
- Do not use outside knowledge.
- Do not hallucinate facts.
- If the answer is not available in the documents, clearly say:
  "The provided documents do not contain enough information."
- Prefer specific names, dates, places, and historical facts from the sources.
- Mention relevant source sections when possible.


USER QUESTION:

{query}



DOCUMENT EVIDENCE:

{context}



FINAL ANSWER:

"""

        return prompt.strip()