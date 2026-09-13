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

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"Page {chunk['page']}:\n{chunk['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an AI PDF assistant.

Answer ONLY from the provided context.

If the answer is not found in the provided context, say exactly:
"I could not find the answer in the document."

When answering:
- Do not use information that is not supported by the context.

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

    if not response.choices:
        print("LLM RESPONSE:", response)
        return "The language model did not return an answer."
    message = response.choices[0].message
    if not message or not message.content:
        return "The language model did not return an answer."
    return message.content
