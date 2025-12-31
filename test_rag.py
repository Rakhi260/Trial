from RAG.rag_pipeline import build_rag, ask_question

# Build vector database (runs once)
collection = build_rag()

# Ask a test question
context = ask_question(
    collection,
    "What courses are offered at Sunbeam?"
)

print("\n--- RETRIEVED CONTEXT ---\n")
print(context)
