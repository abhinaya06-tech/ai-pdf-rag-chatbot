# AI PDF Chatbot

An AI-powered PDF question-answering chatbot built with FastAPI, Streamlit, FAISS, and OpenRouter LLM APIs.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant sections from uploaded PDF documents and generate grounded answers from the retrieved context.

---

## Features

- Upload PDF documents
- Ask natural-language questions about uploaded documents
- Retrieval-Augmented Generation (RAG)
- Page-aware PDF text extraction
- Recursive text chunking with page metadata
- Batched text embedding generation
- Semantic search using normalized embeddings
- Cosine-similarity retrieval with FAISS
- Grounded answers based only on retrieved document context
- Source page citations in generated answers
- FastAPI backend
- Streamlit frontend

---

## How It Works

The application follows this pipeline:

```text
PDF Upload
    ↓
Page-aware PDF Text Extraction
    ↓
Recursive Text Chunking
    ↓
Embedding Generation
    ↓
Embedding Normalization
    ↓
FAISS Vector Index
    ↓
Query Embedding
    ↓
Cosine Similarity Retrieval
    ↓
Relevant Chunks + Page Metadata
    ↓
LLM Response Generation
    ↓
Answer + Source Pages
```

---

## RAG Pipeline

### 1. PDF Processing

Each uploaded PDF is processed page by page using `pypdf`.

Page information is preserved so that retrieved chunks can be associated with their original page numbers.

### 2. Chunking

Extracted text is split using `RecursiveCharacterTextSplitter`.

Each chunk stores:

- chunk text
- page number

### 3. Embeddings

Document chunks are converted into vector embeddings using:

```text
text-embedding-3-small
```

Embeddings are generated in batches and normalized before indexing.

### 4. Vector Search

FAISS is used for vector similarity search.

The application uses:

```text
IndexFlatIP
```

with normalized vectors, which allows inner-product search to represent cosine similarity.

### 5. Retrieval

For each user question:

1. The question is converted into an embedding.
2. The query embedding is normalized.
3. FAISS retrieves the most similar chunks.
4. Retrieved chunks retain their page metadata and similarity scores.

### 6. Grounded Generation

The retrieved chunks are passed to the LLM as context.

The model is instructed to answer only from the provided context. When the answer cannot be found in the retrieved document content, the application returns:

```text
I could not find the answer in the document.
```

### 7. Source Attribution

For supported answers, the generated response includes source page information, for example:

```text
Sources: Page 1, Page 3
```

The API also returns structured source page metadata through:

```json
"source_pages": [1, 3]
```

---

## Tech Stack

- Python
- FastAPI
- Streamlit
- FAISS
- OpenRouter
- OpenAI Python SDK
- PyPDF
- LangChain Text Splitters
- NumPy

---

## Live Demo

### Frontend

https://ai-pdf-rag-chatbot-ixdc2kzlyrkqttezqwx48e.streamlit.app

### Backend

https://ai-pdf-rag-backend.onrender.com

---

## Screenshots

### Home Screen

![Home](assets/home.png)

### PDF Uploaded

![Upload](assets/upload.png)

### Chat Response

![Chat](assets/chat.png)

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/abhinaya06-tech/ai-pdf-rag-chatbot.git
cd ai-pdf-rag-chatbot
```

### Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Do not commit your `.env` file or API key to GitHub.

---

## Run the Backend

```bash
cd backend
uvicorn app:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Run the Frontend

From the project root:

```bash
streamlit run frontend/streamlit_app.py
```

The frontend will run at:

```text
http://localhost:8501
```

---

## API Endpoints

### Upload PDF

```http
POST /upload-pdf
```

Uploads a PDF, extracts its text, creates chunks, generates embeddings, and builds the FAISS index.

Example response:

```json
{
  "message": "document.pdf uploaded successfully",
  "total_chunks": 25
}
```

### Ask a Question

```http
POST /ask
```

Example request:

```json
{
  "question": "What is Python?"
}
```

Example response structure:

```json
{
  "question": "What is Python?",
  "answer": "Python is ... Sources: Page 2",
  "source_pages": [2],
  "retrieved_chunks": []
}
```

---

## Project Structure

```text
ai-pdf-chatbot/
│
├── backend/
│   ├── app.py
│   ├── pdf_loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── vector_store.py
│   └── llm.py
│
├── frontend/
│   └── streamlit_app.py
│
├── assets/
│   ├── home.png
│   ├── upload.png
│   └── chat.png
│
├── requirements.txt
├── render.yaml
├── .gitignore
└── README.md
```

---

## Current Limitations

- Document and vector data are currently stored in application memory.
- The FAISS index is rebuilt when documents are uploaded.
- Upload validation and file-size restrictions can be improved.
- The current architecture does not provide user-level document isolation.
- Retrieval quality can be improved further through evaluation and tuning.

---

## Future Improvements

- Persistent vector storage
- Incremental index updates
- Multi-user document isolation
- Authentication and authorization
- Chat history persistence
- Retrieval evaluation and benchmarking
- Improved PDF parsing for complex layouts
- PDF preview support
- Better frontend UX
- Docker deployment

---

## Author

**Abhinaya Jukanti**

GitHub:

https://github.com/abhinaya06-tech