import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.utils.config import FAISS_INDEX_PATH, FAISS_METADATA_PATH, DOCS_JSON_PATH

# Load FAISS index and metadata
index = faiss.read_index(FAISS_INDEX_PATH)

with open(FAISS_METADATA_PATH, "r", encoding="utf-8") as file:
    metadata = json.load(file)

# Load full document data
with open(DOCS_JSON_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_faiss(query, top_k=5):
    """Retrieve the most relevant documents using FAISS."""
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            doc_url = metadata[idx]["url"]
            doc_details = data.get(doc_url, {})

            result_entry = {
                "url": doc_url,
                "paragraphs": doc_details.get("paragraphs", [])
            }
            results.append(result_entry)

    return results