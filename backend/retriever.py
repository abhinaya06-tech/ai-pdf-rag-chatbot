from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = None

def get_model():
    global model

    if model is None:
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return model


def retrieve(query, index, documents, top_k=3):
    query_embedding = get_model().encode([query])

    D, I = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    retrieved_docs = [documents[i] for i in I[0]]

    return retrieved_docs