import os
import faiss
from sentence_transformers import SentenceTransformer

# print("embed_and_index.py")

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_kb_index(kb_dir):
    """
    Walk through the KB directory, convert all documents to embeddings, and build a FAISS index.
    Returns: FAISS index, original texts, and their file paths.
    """
    texts, paths = [], []

    for root, _, files in os.walk(kb_dir):
        for file in files:
            if file.endswith(".txt") or file.endswith(".md") or file.endswith(".log") or file.endswith(".json"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        texts.append(content)
                        paths.append(full_path)
                except Exception as e:
                    print(f"[ERROR] Could not read {full_path}: {e}")

    if not texts:
        raise ValueError("No KB documents found to index.")

    print(f"[INFO] Encoding {len(texts)} documents from KB...")
    embeddings = model.encode(texts)

    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, texts, paths
