import json
import os
from datetime import datetime



class DocumentManager:


    def __init__(
        self,
        path="data/documents.json"
    ):

        self.path = path


        if not os.path.exists(path):

            with open(
                path,
                "w"
            ) as f:

                json.dump(
                    [],
                    f
                )



    def load(self):

        with open(
            self.path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def save(
        self,
        documents
    ):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                documents,
                f,
                indent=4,
                ensure_ascii=False
            )



    def add(
        self,
        name,
        chunks
    ):

        docs = self.load()


        docs.append({

            "name": name,

            "chunks": chunks,

            "uploaded":
                str(datetime.now()),

            "status":
                "indexed"

        })


        self.save(
            docs
        )



    def all(self):

        return self.load()





    # ==========================
    # DELETE DOCUMENT
    # ==========================


    def remove(
        self,
        document_name
    ):


        docs = self.load()


        updated_docs = []


        removed = False



        for doc in docs:


            # support old format also

            current_name = (

                doc.get("name")

                or

                doc.get("document")

            )


            if current_name == document_name:

                removed = True

                continue



            updated_docs.append(
                doc
            )



        self.save(
            updated_docs
        )


        return removed