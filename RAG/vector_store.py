import chromadb
from chromadb.config import Settings
from RAG.embeddings import embed_texts

def create_vector_store(chunks):
    client = chromadb.Client(
        Settings(
            persist_directory="./chroma",
            anonymized_telemetry=False
        )
    )

    collection = client.get_or_create_collection("sunbeam")

    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            {
                "source": c["source"],
                "title": c["title"],
                "branch": c.get("branch", "")
            }
            for c in chunks
        ],
        ids=[str(i) for i in range(len(texts))]
    )

    # ✅ NO persist() call needed
    return collection
