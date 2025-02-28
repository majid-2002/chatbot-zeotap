from google import genai
from app.utils.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_gemini_response(query, context_docs):
    """Use Gemini to generate a response based on retrieved context."""
    context_str = "\n\n".join([
        f"🔹 **URL:** {doc['url']}\n"
        f"**Paragraphs:** {' '.join(doc['paragraphs'])}\n"
        for doc in context_docs
    ])
    
    prompt = f"""
    - You are an AI assistant helping with Segment documentation.
    Answer the user's query based on the retrieved documentation.
    - The resultant answer should be well detailed and structured as per the documentation provided.
    - Answer should be long enough for the user to understand and grasp the details.

    Context:
    {context_str}

    User Query: "{query}"

    Provide a concise, accurate response.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    return response.text if response else "No response generated."
