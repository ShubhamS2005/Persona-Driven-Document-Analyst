import json
import os



class PersonaManager:


    def __init__(
        self,
        path="modules/persona/personas.json"
    ):

        self.path=path

        self.personas=self.load()



    def load(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def get_persona(
        self,
        name
    ):

        return self.personas.get(
            name
        )



    def all_personas(self):

        return self.personas