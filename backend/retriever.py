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

    # CREATE QUERY EMBEDDING
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = response.data[0].embedding

    # DON'T REQUEST MORE RESULTS THAN AVAILABLE DOCUMENTS
    k = min(top_k, len(documents))

    # SEARCH FAISS INDEX
    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"),
        k
    )

    retrieved_docs = []

    for distance, i in zip(distances[0], indices[0]):

        if i < 0:
            continue

        document = documents[i].copy()

        document["distance"] = float(distance)

        retrieved_docs.append(document)

    return retrieved_docs
