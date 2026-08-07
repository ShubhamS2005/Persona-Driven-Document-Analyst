import spacy
from collections import Counter


class MetadataEnricher:

    def __init__(self):

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

    def extract_entities(self, doc):

        allowed_types = {

            "PERSON",
            "ORG",
            "GPE",
            "LOC",
            "FAC",
            "EVENT"

        }

        entities = []

        for ent in doc.ents:

            if ent.label_ in allowed_types:

                text = ent.text.strip()

                if len(text) > 2:

                    entities.append(text)

        return list(dict.fromkeys(entities))

    def extract_keywords(self, doc):

        words = []

        ignored = {

            "section",
            "instruction",
            "instructions",
            "chapter",
            "page",
            "note"

        }

        for token in doc:

            if (

                token.pos_ in [

                    "NOUN",
                    "PROPN"

                ]

                and not token.is_stop

                and len(token.text) > 3

            ):

                lemma = token.lemma_.lower().strip()

                if (

                    lemma.isalpha()

                    and lemma not in ignored

                ):

                    words.append(
                        lemma
                    )

        keywords = []

        for word, _ in Counter(words).most_common():

            if word not in keywords:

                keywords.append(word)

            if len(keywords) == 10:
                break

        return keywords

    def enrich(self, chunks):

        for chunk in chunks:

            doc = self.nlp(
                chunk["text"]
            )

            entities = self.extract_entities(
                doc
            )

            keywords = self.extract_keywords(
                doc
            )

            chunk["metadata"].update({

                "entities":
                entities,

                "keywords":
                keywords

            })

        return chunks