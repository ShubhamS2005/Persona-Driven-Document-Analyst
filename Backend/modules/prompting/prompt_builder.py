class PromptBuilder:


    def build(
        self,
        query,
        context,
        persona
    ):


        persona_name = persona.get(
            "persona",
            "general assistant"
        )


        confidence = persona.get(
            "confidence",
            0
        )


        prompt=f"""

You are an AI assistant.

Detected User Context:
{persona_name}


Persona Confidence:
{confidence:.2f}


Behavior:

Adapt your answer according to the detected context.

- If the document is technical:
  explain architecture, concepts and implementation details.

- If the document is a resume:
  provide career-focused analysis, skills, projects and improvement suggestions.

- If the document is historical:
  explain timeline, events and cultural context.

- If the document is travel related:
  provide practical recommendations.


GROUNDING RULES:

- Answer only from the provided document evidence.
- Do not use external knowledge.
- Do not invent missing information.
- If evidence is insufficient say:
  "The provided documents do not contain enough information."


USER QUESTION:

{query}



DOCUMENT EVIDENCE:

{context}



FINAL ANSWER:

"""


        return prompt.strip()