import json


from modules.pipeline.full_pipeline import FullRAGPipeline
from modules.evaluation.evaluator import RAGEvaluator



EVAL_DATA = "data/evaluation/questions.json"



def load_questions():


    with open(
        EVAL_DATA,
        encoding="utf-8"
    ) as f:

        return json.load(f)





def main():


    print(
        "\nInitializing Pipeline..."
    )


    pipeline = FullRAGPipeline()


    evaluator = RAGEvaluator()



    questions = load_questions()



    results=[]



    print(
        "\nStarting Evaluation\n"
    )



    for item in questions:


        print(
            "="*60
        )


        print(
            "QUESTION:"
        )

        print(
            item["query"]
        )



        # run complete pipeline

        output = pipeline.run(
            item["query"]
        )



        report = evaluator.evaluate(
            output,
            item
        )


        results.append(
            report
        )



        print(
            "\nEvaluation:"
        )


        print(
            json.dumps(
                report,
                indent=2
            )
        )





    print(
        "\n\nFINAL REPORT"
    )


    print(
        "="*60
    )



    avg={}



    keys=results[0].keys()



    for key in keys:


        avg[key]=sum(

            r[key]

            for r in results

        ) / len(results)



    print(
        json.dumps(
            avg,
            indent=4
        )
    )




if __name__=="__main__":

    main()