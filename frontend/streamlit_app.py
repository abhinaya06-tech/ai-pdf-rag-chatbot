import streamlit as st
import requests


# RENDER BACKEND URL
BACKEND_URL = "https://ai-pdf-rag-backend.onrender.com"


st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📄",
    layout="wide"
)


# SESSION STATE

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []


# SIDEBAR

with st.sidebar:

    st.header("Upload PDFs")

    uploaded_files = st.file_uploader(
        "Choose PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:

        for uploaded_file in uploaded_files:

            # Avoid duplicate uploads
            if uploaded_file.name not in st.session_state.uploaded_files:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        "application/pdf"
                    )
                }

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/upload-pdf",
                        files=files
                    )

                    if response.status_code == 200:

                        st.session_state.uploaded_files.append(
                            uploaded_file.name
                        )

                    else:

                        st.error(
                            f"Upload failed: {response.text}"
                        )

                except Exception as e:

                    st.error(f"Error: {e}")

        st.success("PDFs uploaded successfully!")


    st.subheader("Uploaded Documents")

    for file_name in st.session_state.uploaded_files:

        st.write(f"📄 {file_name}")


# MAIN UI

st.title("📄 AI PDF Chatbot")


# CHAT HISTORY

for chat in st.session_state.chat_history:

    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])

        with st.expander("Retrieved Context"):

            for i, chunk in enumerate(chat["chunks"]):

                st.markdown(f"### Chunk {i+1}")
                st.write(chunk)


# CHAT INPUT

question = st.chat_input(
    "Ask a question about your PDFs"
)


if question:

    payload = {
        "question": question
    }

    try:

        response = requests.post(
            f"{BACKEND_URL}/ask",
            json=payload
        )

        data = response.json()

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": data.get(
                    "answer",
                    "No answer returned."
                ),
                "chunks": data.get(
                    "retrieved_chunks",
                    []
                )
            }
        )

        st.rerun()

    except Exception as e:

        st.error(f"Error: {e}")