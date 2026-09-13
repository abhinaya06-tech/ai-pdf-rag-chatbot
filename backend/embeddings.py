from openai import OpenAI
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def create_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    embeddings = [
        item.embedding
        for item in response.data
    ]

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    # Normalize embeddings for cosine similarity
    norms = np.linalg.norm(
        embeddings,
        axis=1,
        keepdims=True
    )

    embeddings = embeddings / np.maximum(
        norms,
        1e-12
    )

    return embeddings.tolist()