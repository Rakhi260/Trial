from RAG.loader import load_sunbeam_data
from RAG.chunker import chunk_text
from RAG.vector_store import create_vector_store

def build_rag():
    docs = load_sunbeam_data()
    chunks = []

    for d in docs:
        for ch in chunk_text(d["text"]):
            chunks.append({
                "text": ch,
                "source": d["source"],
                "title": d["title"]
            })

    return create_vector_store(chunks)

def ask_question(collection, query):
    results = collection.query(
        query_texts=[query],
        n_results=4
    )

    documents = results.get("documents", [[]])[0]
    context = "\n".join(documents)

    return context
