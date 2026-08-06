from modules.llm.llm_client import LLMClient



if __name__=="__main__":


    llm=LLMClient()


    prompt="""

    Explain Carcassonne medieval architecture
    in simple words.

    """


    answer=llm.generate(
        prompt
    )


    print("\nANSWER\n")

    print(answer)