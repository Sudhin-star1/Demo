import faiss
import pickle
from sentence_transformers import SentenceTransformer

def load_index(path='faiss_index'):
    index = faiss.read_index(f'{path}/index.faiss')
    with open(f'{path}/chunks.pkl', 'rb') as f:
        chunks, model_name = pickle.load(f)
    return index, chunks

def retrieve_top_k(query, k=3, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    query_vec = model.encode([query])
    index, chunks = load_index()
    D, I = index.search(query_vec, k)
    # For no results found
    if len(I[0]) == 0: 
        return ["No relevant context found."]
    return [chunks[i] for i in I[0]]
