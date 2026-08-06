class ContextBuilder:


    def __init__(
        self,
        max_sources=5
    ):

        self.max_sources=max_sources



    def build(
        self,
        retrieved_chunks,
        persona=None
    ):


        context=[]



        if persona:


            context.append(
                "USER PERSONA\n"
            )


            context.append(

                f"""
Role:
{persona['persona']}

Answer Style:
{persona['details']['style']}

Focus Areas:
{', '.join(persona['details']['focus'])}

"""
            )



        context.append(
            "\nDOCUMENT SOURCES\n"
        )



        for idx,chunk in enumerate(
            retrieved_chunks[:self.max_sources],
            start=1
        ):


            metadata=chunk["metadata"]


            source=f"""

===== SOURCE {idx} =====

Document:
{metadata.get('document')}

Section:
{metadata.get('section_title')}

Pages:
{metadata.get('page_start')}
-
{metadata.get('page_end')}


Content:

{chunk['text']}

"""


            context.append(
                source
            )



        return "\n".join(context)