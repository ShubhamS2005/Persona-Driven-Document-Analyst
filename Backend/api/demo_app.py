from flask import Flask, request, jsonify
from flask_cors import CORS
import os


app = Flask(__name__)

CORS(app)


pipeline = None


def get_pipeline():

    global pipeline

    if pipeline is None:

        print("Loading RAG pipeline...")


        from modules.pipeline.full_pipeline import FullRAGPipeline
        from modules.retrieval.retriever import Retriever


        retriever = Retriever(
            demo=True
        )


        pipeline = FullRAGPipeline(
            retriever=retriever
        )


        print("Pipeline ready")


    return pipeline



@app.route("/health")
def health():

    return jsonify({
        "status":"running",
        "mode":"demo"
    })

@app.route("/")
def home():

    return jsonify({
        "status":"running",
        "mode":"demo",
        "info":"ask questions from uploaded docs"
    })

@app.route("/documents", methods=["GET"])
def get_documents():

    return jsonify({
        "documents": [
            {
                "name": "Resume.pdf",
                "mode": "demo"
            },
            {
                "name": "Dishes.pdf",
                "mode": "demo"
            },
            {
                "name": "Cities_South.pdf",
                "mode": "demo"
            }
        ]
    })


@app.route("/ask", methods=["POST"])
def ask():

    data=request.json

    query=data.get("query")


    rag_pipeline=get_pipeline()


    result=rag_pipeline.run(query)


    return jsonify({

        "answer":result["answer"],

        "persona":result["persona"],

        "sources":[
            {
                "document":c["metadata"]["document"]
            }
            for c in result["retrieved"]
        ]

    })



if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT",5000))
    )