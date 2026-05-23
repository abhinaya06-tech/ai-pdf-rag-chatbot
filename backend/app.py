from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil

from pdf_loader import load_pdf
from chunking import chunk_text
from embeddings import create_embeddings
from vector_store import create_faiss_index
from retriever import retrieve_chunks
from llm import generate_response


app = FastAPI()


# GLOBAL VARIABLES

all_chunks = []
index = None


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():

    return {
        "message": "AI PDF Chatbot Backend Running"
    }


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    global all_chunks
    global index

    file_path = f"../data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = load_pdf(file_path)

    new_chunks = chunk_text(text)

    all_chunks.extend(new_chunks)

    embeddings = create_embeddings(all_chunks)

    index = create_faiss_index(embeddings)

    return {
        "message": f"{file.filename} uploaded successfully",
        "total_chunks": len(all_chunks)
    }


@app.post("/ask")
def ask_question(request: QueryRequest):

    global all_chunks
    global index

    if len(all_chunks) == 0 or index is None:

        return {
            "error": "Please upload a PDF first."
        }

    # Split combined questions
    questions = request.question.lower().split(" and ")

    retrieved_chunks = []

    for q in questions:

        chunks = retrieve_chunks(
            q,
            index,
            all_chunks
        )

        retrieved_chunks.extend(chunks)

    # Remove duplicate chunks
    retrieved_chunks = list(dict.fromkeys(retrieved_chunks))

    response = generate_response(
        request.question,
        retrieved_chunks
    )

    return {
        "question": request.question,
        "answer": response,
        "retrieved_chunks": retrieved_chunks
    }