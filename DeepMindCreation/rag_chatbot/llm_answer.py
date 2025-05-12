from langchain_ollama import OllamaLLM

def ask_llm(query, context):
    # Initializing the OllamaLLM with llama3.2 model
    llm = OllamaLLM(model="llama3.2", temperature=0.1)
    
    prompt = f"""You are a helpful assistant. Use the context below to answer the question.

    Context:
    {context}

    Question: {query}
    Answer:"""
        
    response = llm.invoke(prompt)
    return response.strip()