from sentence_transformers import SentenceTransformer

model = None


def get_embedding_model():
    global model

    if model is None:
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return model


def generate_embeddings(texts):
    model = get_embedding_model()
    return model.encode(texts)