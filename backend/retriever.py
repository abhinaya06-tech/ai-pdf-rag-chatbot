from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def retrieve_chunks(
    query,
    index,
    documents,
    top_k=3
):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = np.array(
        response.data[0].embedding,
        dtype="float32"
    )

    # Normalize query embedding for cosine similarity
    query_embedding = query_embedding / max(
        np.linalg.norm(query_embedding),
        1e-12
    )

    k = min(top_k, len(documents))

    similarities, indices = index.search(
        np.array([query_embedding]),
        k
    )

    retrieved_docs = []

    for similarity, i in zip(similarities[0], indices[0]):
        if i < 0:
            continue

        document = documents[i].copy()
        document["similarity"] = float(similarity)
        retrieved_docs.append(document)

    return retrieved_docs