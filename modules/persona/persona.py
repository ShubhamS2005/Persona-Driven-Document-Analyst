class PersonaManager:


    def build_prompt_style(
        self,
        persona
    ):


        styles = {


            "technical mentor":

            """
Answer with technical depth.
Explain architecture,
implementation details,
tradeoffs and engineering decisions.
""",



            "research analyst":

            """
Answer with analytical reasoning,
comparisons,
methodology and evidence.
""",



            "career advisor":

            """
Answer with practical career guidance,
resume improvement,
skills and actionable suggestions.
""",



            "historical analyst":

            """
Answer with timeline,
historical context,
events and cultural explanation.
""",



            "travel advisor":

            """
Answer with practical recommendations,
locations and planning advice.
""",



            "general assistant":

            """
Answer clearly and concisely.
"""

        }



        return styles.get(

            persona,

            styles["general assistant"]

        )