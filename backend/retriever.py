import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def retrieve_chunks(
    query,
    index,
    chunks,
    top_k=5,
    similarity_threshold=1.5
):

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    retrieved_chunks = []

    for i, idx in enumerate(indices[0]):

        if idx == -1:
            continue

        distance = distances[0][i]

        # lower distance = better similarity
        if distance < similarity_threshold:

            retrieved_chunks.append(chunks[idx])

    return retrieved_chunks