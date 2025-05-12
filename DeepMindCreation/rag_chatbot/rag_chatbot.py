import torch
torch.set_num_threads(1)

import pickle
import faiss
from sentence_transformers import SentenceTransformer
from llm_answer import ask_llm
from retriever import retrieve_top_k


if __name__ == "__main__":
    print("RAG Chatbot ready. Ask a question!")
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            break
        context = retrieve_top_k(query)
        answer = ask_llm(query, context)
        print(f"Bot: {answer}")