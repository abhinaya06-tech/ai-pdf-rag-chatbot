from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

from pdf_loader import load_pdf
from chunking import chunk_text
from embeddings import create_embeddings
from vector_store import create_faiss_index
from retriever import retrieve_chunks
from llm import generate_response


app = FastAPI()


# CREATE DATA FOLDER
os.makedirs("data", exist_ok=True)


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

    # SAVE FILE
    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # LOAD PDF TEXT
    text = load_pdf(file_path)

    # CHUNK TEXT
    new_chunks = chunk_text(text)

    # STORE CHUNKS
    all_chunks.extend(new_chunks)

    # CREATE EMBEDDINGS
    embeddings = create_embeddings(all_chunks)

    # CREATE FAISS INDEX
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

    # RETRIEVE RELEVANT CHUNKS
    retrieved_chunks = retrieve_chunks(
        request.question,
        index,
        all_chunks
    )

    # GENERATE RESPONSE
    response = generate_response(
        request.question,
        retrieved_chunks
    )

    return {
        "question": request.question,
        "answer": response,
        "retrieved_chunks": retrieved_chunks
    }