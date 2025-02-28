

# Chatbot Web Interface  

A simple chatbot web interface built using HTML, CSS, and JavaScript. This project provides a frontend for interacting with a chatbot API.  Checkout the [Website](https://shorturl.at/E5bhU) for the chatbot.

## Overview 

This chatbot is built using FAISS for vector search and Gemini AI as the NLP model. It enables Retrieval-Augmented Generation (RAG) by fetching relevant document chunks and passing them to Gemini for generating responses.
Responses generated are from [Segment Docs](https://segment.com/docs).



## 🛠️ Tech Stack  

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask) 
- **Vector Database:** FAISS (Facebook AI Similarity Search)
- **NLP Model:** Gemini AI (Google’s LLM)
- **Data Processing:** BeautifulSoup / Scrapy for web scraping




## 📦 Installation & Running  

### 1️⃣ Clone the Repository  

```sh
git clone https://github.com/majid-2002/chatbot-zeotap.git
cd chatbot-zeotap
```
### 2️⃣ Start the Server

```sh
pip install -r requirements.txt
python3 run.py
```

### 3️⃣ Open the Web Interface
```sh
http://localhost:5000
```


