from llm_answer import ask_llm

# Example testing
context = "The sun is the star at the center of the solar system. It provides light and heat to Earth."
question = "What is the sun and why is it important?"

response = ask_llm(question, context)

print("LLM Answer:", response)
