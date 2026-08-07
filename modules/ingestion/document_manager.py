import json
import os
from datetime import datetime



class DocumentManager:


    def __init__(
        self,
        path="data/documents.json"
    ):

        self.path=path


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
            self.path
        ) as f:

            return json.load(f)



    def save(
        self,
        documents
    ):

        with open(
            self.path,
            "w"
        ) as f:

            json.dump(
                documents,
                f,
                indent=4
            )



    def add(
        self,
        name,
        chunks
    ):


        docs=self.load()


        docs.append({

            "name":
            name,


            "chunks":
            chunks,


            "uploaded":
            str(
                datetime.now()
            ),


            "status":
            "indexed"

        })


        self.save(
            docs
        )



    def all(self):
        data = self.load()

        print("LOAD TYPE:", type(data))
        print("LOAD VALUE:", data)
        return data