# 🧠 RAG-Based Chatbot

A simple chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions based on a document.

# Prerequisites

Install Ollama to run the LLM locally.
https://ollama.com/download/mac (or suitable OS)

In terminal: ollama run llama3.2

Running the LLMs locally ensures the data privacy and data theft protection.

## Setup

```bash
pip install -r requirements.txt
python ingest.py
python rag_chatbot.py
```

## If any error regarding Numpy not found:
pip install numpy==1.26.4