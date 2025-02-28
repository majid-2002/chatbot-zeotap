import os

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

# Correct FAISS index and metadata file paths
FAISS_INDEX_PATH = os.path.join(DATA_DIR, "faiss_index.bin")
FAISS_METADATA_PATH = os.path.join(DATA_DIR, "faiss_metadata.json")
DOCS_JSON_PATH = os.path.join(DATA_DIR, "segment_docs.json")

# Ensure the "data" directory exists
os.makedirs(DATA_DIR, exist_ok=True)
# Sentence Transformer model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Raise an error if the API key is missing
if not GEMINI_API_KEY:
    raise ValueError("Missing Google Gemini API key. Set GEMINI_API_KEY in your environment variables.")
