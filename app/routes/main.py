from flask import Blueprint, request, jsonify, render_template
from app.utils.search import search_faiss
from app.utils.gemini import generate_gemini_response

main = Blueprint("main", __name__)

@main.route("/") 
def home():
    return render_template("index.html")


@main.route("/query", methods=["POST"])
def query():
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query parameter is missing"}), 400

    retrieved_docs = search_faiss(user_query)
    gemini_response = generate_gemini_response(user_query, retrieved_docs)

    return jsonify({"query": user_query, "response": gemini_response})
