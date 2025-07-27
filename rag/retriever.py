from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# print("retreiver.py")

def retrieve_relevant_kb(index, query, texts, top_k=3):
    """
    Given a FAISS index and a query (string), retrieve the top_k most relevant documents from the knowledge base.
    Returns a list of top-k text snippets.
    """
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(texts):
            results.append(texts[idx])
    return results
