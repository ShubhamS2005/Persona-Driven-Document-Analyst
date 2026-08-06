import os

from dotenv import load_dotenv
from google import genai



class LLMClient:


    def __init__(self):

        load_dotenv()


        api_key = os.getenv(
            "GOOGLE_API_KEY"
        )


        if not api_key:

            raise ValueError(
                "GOOGLE_API_KEY missing"
            )


        self.client = genai.Client(
            api_key=api_key
        )


        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "models/gemini-flash-latest"
        )



    def generate(
        self,
        prompt
    ):


        response = self.client.models.generate_content(

            model=self.model_name,

            contents=prompt

        )


        return response.text