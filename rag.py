from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")
index = None
metadata_store = []

def chunk_code(text, path):
    lines = text.split("\n")
    chunks = []
    current = []

    for line in lines:
        current.append(line)

        if line.strip().startswith(("def ", "class ", "function ")):
            if len(current) > 20:
                chunks.append("\n".join(current))
                current = []

    if current:
        chunks.append("\n".join(current))

    final_chunks = []
    for chunk in chunks:
        if len(chunk) > 800:
            for i in range(0, len(chunk), 400):
                final_chunks.append(chunk[i:i+400])
        else:
            final_chunks.append(chunk)

    return [{"text": c, "path": path} for c in final_chunks]

def add(files):
    global index

    all_chunks = []

    for f in files:
        chunks = chunk_code(f["content"], f["path"])
        all_chunks.extend(chunks)

    if not all_chunks:
        return  

    texts = [c["text"] for c in all_chunks]

    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)

    if index is None:
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)

    index.add(embeddings)
    metadata_store.extend(all_chunks)

def search(query, k=5):
    if index is None or not metadata_store:
        return []
    query_vec = model.encode([query]).astype("float32")
    faiss.normalize_L2(query_vec)

    k = min(k, len(metadata_store))  
    scores, indices = index.search(query_vec, k)
    results = []
    seen = set()
    for idx in indices[0]:
        if idx >= len(metadata_store):  
            continue
        item = metadata_store[idx]
        key = (item["path"], item["text"][:50])
        if key in seen:
            continue

        seen.add(key)
        results.append((item["text"], item["path"]))

    return results
def reset():
    global index, metadata_store
    index = None
    metadata_store = []