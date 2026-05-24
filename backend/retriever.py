from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def retrieve_chunks(query, index, documents, top_k=3):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = response.data[0].embedding

    D, I = index.search(
        np.array([query_embedding]).astype("float32"),
        top_k
    )

    retrieved_docs = [documents[i] for i in I[0]]

    return retrieved_docs