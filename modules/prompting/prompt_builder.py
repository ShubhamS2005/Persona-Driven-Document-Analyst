class PromptBuilder:



    def build(
        self,
        query,
        context,
        persona
    ):


        prompt=f"""

You are an AI assistant answering as:

{persona['persona']}


Answer style:

{persona['details']['style']}


Instructions:

- Use only the provided document context.
- Do not invent facts.
- Mention sources when possible.
- Follow the persona perspective.


USER QUESTION:

{query}



CONTEXT:

{context}



FINAL ANSWER:

"""


        return prompt.strip()