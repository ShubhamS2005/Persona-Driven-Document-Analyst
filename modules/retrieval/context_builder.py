class ContextBuilder:


    def __init__(
        self,
        max_sources=5
    ):

        self.max_sources = max_sources



    def build(
        self,
        retrieved_chunks,
        persona=None
    ):


        context = []



        if persona:


            context.append(
                "USER PERSONA\n"
            )


            context.append(

f"""
Detected Persona:
{persona.get('persona','general assistant')}

Confidence:
{persona.get('confidence',0):.2f}

"""
            )



        context.append(
            "\nDOCUMENT SOURCES\n"
        )



        for idx, chunk in enumerate(
            retrieved_chunks[:self.max_sources],
            start=1
        ):


            metadata = chunk.get(
                "metadata",
                {}
            )


            source=f"""

===== SOURCE {idx} =====

Document:
{metadata.get('document','Unknown')}


Section:
{metadata.get('section_title','Unknown')}


Pages:
{metadata.get('page_start')}
-
{metadata.get('page_end')}


Keywords:
{', '.join(metadata.get('keywords',[]))}


Entities:
{', '.join(metadata.get('entities',[]))}


Content:

{chunk.get('text','')}

"""


            context.append(source)



        return "\n".join(context)