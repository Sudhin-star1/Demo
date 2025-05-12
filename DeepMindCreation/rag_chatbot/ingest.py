from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import faiss
import os
import pickle

EMBED_MODEL = 'all-MiniLM-L6-v2'

def load_pdf(path):
    reader = PdfReader(path)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def build_faiss_index(chunks, embed_model_name=EMBED_MODEL):
    model = SentenceTransformer(embed_model_name)
    embeddings = model.encode(chunks, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, chunks, embed_model_name

def save_index(index, chunks, model_name, path='faiss_index'):
    os.makedirs(path, exist_ok=True)
    faiss.write_index(index, f'{path}/index.faiss')
    with open(f'{path}/chunks.pkl', 'wb') as f:
        pickle.dump((chunks, model_name), f)  # saving tuple

if __name__ == '__main__':
    text = load_pdf("data/sample.pdf")
    chunks = chunk_text(text)
    index, chunks, model_name = build_faiss_index(chunks)
    save_index(index, chunks, model_name)
    print("FAISS index and chunks saved successfully.")