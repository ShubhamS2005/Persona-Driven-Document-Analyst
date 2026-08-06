class ContextBuilder:


    def __init__(
        self,
        max_context_length=None
    ):

        self.max_context_length = max_context_length



    def build(
        self,
        retrieved_chunks
    ):


        if not retrieved_chunks:

            return ""



        context_parts=[]



        for idx,chunk in enumerate(
            retrieved_chunks,
            start=1
        ):


            metadata = chunk.get(
                "metadata",
                {}
            )


            document = metadata.get(
                "document",
                "Unknown"
            )


            section = metadata.get(
                "section_title",
                "Unknown"
            )


            page_start = metadata.get(
                "page_start",
                "?"
            )


            page_end = metadata.get(
                "page_end",
                "?"
            )



            text = chunk.get(
                "text",
                ""
            )



            source_block = f"""

===== SOURCE {idx} =====

Document:
{document}

Section:
{section}

Page:
{page_start} - {page_end}


Content:

{text}

"""


            context_parts.append(
                source_block.strip()
            )



        context="\n\n".join(
            context_parts
        )


        if self.max_context_length:

            context=context[
                :self.max_context_length
            ]


        return context