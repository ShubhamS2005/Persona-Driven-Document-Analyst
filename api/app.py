from flask import Flask, request, jsonify
from flask_cors import CORS

from modules.pipeline.full_pipeline import FullRAGPipeline

app = Flask(__name__)
CORS(app)

print("Starting RAG API...")
pipeline = FullRAGPipeline()
print("API Ready")

@app.route( "/health", methods=["GET"])
def health():
    return jsonify({
        "status":
        "running",
        "service":
        "Persona RAG API"

    })


@app.route("/ask", methods=["POST"])
def ask():
    data=request.json
    query=data.get(
        "query"
    )

    result = pipeline.run(
        query
    )
    sources=[]


    for chunk in result["retrieved"]:
        sources.append({

            "document":
            chunk["metadata"].get(
                "document"
            ),


            "section":
            chunk["metadata"].get(
                "section_title"
            ),


            "pages":
            (
            chunk["metadata"].get(
                "page_start"
            ),
            chunk["metadata"].get(
                "page_end"
            )
            ),


            "score":
            chunk["score"]

        })

    return jsonify({
        "query":
        query,

        "persona":
        {
            "name":
            result["persona"]["persona"],

            "confidence":
            result["persona"]["confidence"]
        },

        "answer":
        result["answer"],

        "sources":
        sources

    })





if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )