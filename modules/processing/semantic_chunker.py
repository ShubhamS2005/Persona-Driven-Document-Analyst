from transformers import AutoTokenizer


class SemanticChunker:

    def __init__(
        self,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

    def count_tokens(self, text):

        return len(
            self.tokenizer.encode(
                text,
                add_special_tokens=False
            )
        )

    def build_section_text(self, section):

        title = section.get(
            "title",
            ""
        )

        contents = section.get(
            "content",
            []
        )

        body = " ".join(
            [
                item.strip()
                for item in contents
                if item.strip()
            ]
        )

        # Keep title for semantic context
        if title:

            return f"""
{title}

{body}
""".strip()

        return body.strip()

    def create_chunks(
        self,
        sections,
        chunk_size=500,
        overlap=70,
        min_tokens=50
    ):

        chunks = []

        chunk_id = 0

        for section in sections:

            full_text = self.build_section_text(
                section
            )

            if not full_text:
                continue

            tokens = self.tokenizer.encode(
                full_text,
                add_special_tokens=False
            )

            start = 0

            while start < len(tokens):

                end = start + chunk_size

                chunk_tokens = tokens[start:end]

                chunk_text = self.tokenizer.decode(
                    chunk_tokens,
                    skip_special_tokens=True
                ).strip()

                token_count = len(chunk_tokens)

                if token_count >= min_tokens:

                    chunks.append({

                        "id": chunk_id,

                        "text": chunk_text,

                        "metadata": {

                            "document":
                            section["document"],

                            "source":
                            section.get(
                                "source",
                                ""
                            ),

                            "section_title":
                            section.get(
                                "title",
                                "Unknown"
                            ),

                            "page_start":
                            section.get(
                                "page_start"
                            ),

                            "page_end":
                            section.get(
                                "page_end"
                            ),

                            "chunk_index":
                            chunk_id,

                            "token_count":
                            token_count

                        }

                    })

                    chunk_id += 1

                start = end - overlap

                if start < 0:
                    start = 0

        return chunks