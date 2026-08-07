from flask import Flask,request,jsonify
from flask_cors import CORS

from modules.pipeline.full_pipeline import FullRAGPipeline
from modules.retrieval.retriever import Retriever


app = Flask(__name__)

CORS(app)


retriever = Retriever(
    demo=True
)


pipeline = FullRAGPipeline(
    retriever=retriever
)



@app.route("/health")
def health():

    return {
        "status":"running",
        "mode":"demo"
    }



@app.route("/ask",methods=["POST"])
def ask():

    data=request.json

    query=data["query"]


    result=pipeline.run(query)


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
        port=5000
    )