from pdf_loader import load_pdf
from chunking import chunk_text
from embeddings import create_embeddings
from vector_store import create_faiss_index
from retriever import retrieve_chunks
from llm import generate_response


text = load_pdf("../data/sample.pdf")

chunks = chunk_text(text)

embeddings = create_embeddings(chunks)

index = create_faiss_index(embeddings)

query = "What is Python?"

retrieved_chunks = retrieve_chunks(query, index, chunks)

response = generate_response(query, retrieved_chunks)

print("\nAI RESPONSE:\n")

print(response)