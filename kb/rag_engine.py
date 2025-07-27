def build_kb_index(kb_path):
    texts = []
    paths = []

    for root, _, files in os.walk(kb_path):
        for file in files:
            with open(os.path.join(root, file), "r") as f:
                texts.append(f.read())
                paths.append(os.path.join(root, file))

    embeddings = embed_texts(texts)
    index = FAISS.from_embeddings(embeddings)

    return index, texts, paths
