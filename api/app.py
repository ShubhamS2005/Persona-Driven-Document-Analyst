from flask import Flask, request, jsonify,Blueprint
from flask_cors import CORS
import os
from modules.pipeline.full_pipeline import FullRAGPipeline
from modules.pipeline.ingestion_pipeline import IngestionPipeline
from modules.retrieval.retriever import Retriever
from modules.ingestion.document_manager import DocumentManager

app = Flask(__name__)
CORS(app)

upload_bp = Blueprint("upload",__name__)
UPLOAD_FOLDER="data/uploads"


print("Starting RAG API...")
retriever = Retriever()
pipeline = FullRAGPipeline(retriever=retriever)
ingestion = IngestionPipeline()
document_manager = DocumentManager()
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
        "query":query,
        "persona":
{
            "name":
            result["persona"]["persona"],

            "confidence":
            result["persona"]["confidence"]
        },

        "answer":result["answer"],
        "sources":sources,
        "retrieved_chunks": len(result["retrieved"])

    })

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"error": "No file selected"}, 400

    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are supported"}, 400

    path = os.path.join("data/input_pdfs",file.filename)

    file.save(path)

    result = ingestion.ingest_pdf(path)

    retriever.refresh()

    document_manager.add(result["document"],result["chunks"])

    return {
        "message":
        "Document indexed successfully",

        "document":
        result["document"],

        "chunks":
        result["chunks"]

    }

@app.route("/documents", methods=["GET"])
def get_documents():

    documents = document_manager.all()

    print("TYPE:", type(documents))
    print("VALUE:", documents)

    response = {
        "documents": documents
    }

    print("RESPONSE:", response)
    print("RESPONSE TYPE:", type(response["documents"]))

    return jsonify(response)

if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )