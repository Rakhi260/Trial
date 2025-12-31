def retrieve_docs(collection, query, k=4):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    return results["documents"][0]
