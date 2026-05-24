from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def generate_response(
    query,
    retrieved_chunks
):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an AI PDF assistant.

Answer ONLY from the provided context.

If answer is not found, say:
"I could not find the answer in the document."

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content