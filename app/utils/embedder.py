import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load JSON file
with open("segment_docs.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Extract text content for indexing
documents = []
metadata = []

for url, page in data.items():  # Iterate over dictionary keys (URLs) and values (page data)
    headings_text = " ".join([" ".join(page["headings"].get(h, [])) for h in page["headings"]])
    
    text_content = " ".join([
        headings_text,
        " ".join(page.get("paragraphs", [])),
        " ".join([" ".join(lst) for lst in page["lists"].get("unordered", [])]),
        " ".join([" ".join(lst) for lst in page["lists"].get("ordered", [])]),
        " ".join(page.get("code_blocks", [])),
        " ".join(page.get("blockquotes", [])),
    ]).strip()

    if text_content:  # Avoid indexing empty pages
        documents.append(text_content)
        metadata.append({"url": url})

# Convert documents to embeddings
if documents:
    embeddings = model.encode(documents, show_progress_bar=True)
    embeddings = np.array(embeddings, dtype="float32")

    # Create FAISS index
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, "faiss_index.bin")

    # Save metadata
    with open("faiss_metadata.json", "w", encoding="utf-8") as meta_file:
        json.dump(metadata, meta_file, indent=4)

    print(f"✅ Indexed {len(documents)} documents and saved FAISS index.")
else:
    print("❌ No valid text content found to index.")
