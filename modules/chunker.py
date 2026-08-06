import re
from typing import List, Dict



def clean_chunk_text(text: str):

    # Remove bullet artifacts
    text = re.sub(
        r"\n\s*[•●▪]\s*",
        "\n",
        text
    )


    # Remove repeated spaces/newlines
    text = re.sub(
        r"\s+",
        " ",
        text
    )


    return text.strip()



def remove_heading_prefix(text, section_title):

    if not section_title:
        return text


    title_clean = section_title.strip()


    if text.lower().startswith(
        title_clean.lower()
    ):
        return text[
            len(title_clean):
        ].strip()


    return text



def split_text(
    text,
    chunk_size=500,
    overlap=100
):

    words = text.split()


    if len(words)<=chunk_size:
        return [
            text.strip()
        ]


    chunks=[]

    start=0


    while start < len(words):

        end=start+chunk_size


        chunks.append(
            " ".join(
                words[start:end]
            )
        )


        start=end-overlap


    return chunks




def create_chunks(
    sections: List[Dict]
):

    final_chunks=[]


    for section in sections:


        raw_text=section.get(
            "body_text",
            ""
        )


        section_title=section.get(
            "section_title",
            ""
        )


        if not raw_text:
            continue


        text=clean_chunk_text(
            raw_text
        )

        text=remove_common_heading_prefix(text)

        text=remove_heading_prefix(
            text,
            section_title
        )


        if len(text.split()) < 20:
            continue



        chunks=split_text(
            text
        )


        for idx,chunk in enumerate(chunks):


            final_chunks.append(

                {
                    "id":
                    len(final_chunks),

                    "text":
                    chunk,

                    "metadata":
                    {

                    "document":
                    section.get("doc"),

                    "page":
                    section.get("page"),

                    "section":
                    section_title,

                    "chunk_index": idx

                    }
                }

            )


    return final_chunks

def remove_common_heading_prefix(text):

    common_headings = [
        "Introduction",
        "Overview",
        "Summary",
        "Conclusion"
    ]

    for heading in common_headings:

        if text.startswith(heading):

            text = text[len(heading):].strip()

    return text