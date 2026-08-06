from modules.pipeline.full_pipeline import FullRAGPipeline



if __name__=="__main__":


    pipeline = FullRAGPipeline()



    query = (
        "What are the historical sites in Carcassonne?"
    )



    response = pipeline.run(
        query
    )



    print("\n\nFINAL ANSWER\n")


    print(
        response["answer"]
    )