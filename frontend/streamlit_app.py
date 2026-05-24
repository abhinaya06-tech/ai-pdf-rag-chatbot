import streamlit as st
import requests

# -----------------------------
# CONFIG
# -----------------------------
BACKEND_URL = "https://ai-pdf-rag-backend.onrender.com"

st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("Upload PDFs")

    uploaded_files = st.file_uploader(
        "Choose PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    # Upload PDFs only once
    if uploaded_files and not st.session_state.uploaded:

        with st.spinner("Uploading and processing PDFs..."):

            try:
                files = [
                    (
                        "files",
                        (
                            file.name,
                            file.getvalue(),
                            "application/pdf"
                        )
                    )
                    for file in uploaded_files
                ]

                response = requests.post(
                    f"{BACKEND_URL}/upload-pdf",
                    files=files,
                    timeout=300
                )

                if response.status_code == 200:
                    st.success("PDFs uploaded successfully!")

                    st.session_state.uploaded = True

                    st.session_state.uploaded_files = [
                        file.name for file in uploaded_files
                    ]

                else:
                    st.error(f"Upload failed: {response.text}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.subheader("Uploaded Documents")

    for file_name in st.session_state.uploaded_files:
        st.write(f"📄 {file_name}")

    if st.button("Reset PDFs"):
        st.session_state.uploaded = False
        st.session_state.uploaded_files = []
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# MAIN UI
# -----------------------------
st.title("📄 AI PDF Chatbot")

# Display chat messages
for role, message in st.session_state.messages:

    with st.chat_message(role):
        st.markdown(message)

# -----------------------------
# CHAT INPUT
# -----------------------------
question = st.chat_input("Ask a question about your PDFs")

if question:

    # Show user message
    st.session_state.messages.append(("user", question))

    with st.chat_message("user"):
        st.markdown(question)

    # Get AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={"question": question},
                    timeout=300
                )

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer returned."
                    )

                    st.markdown(answer)

                    st.session_state.messages.append(
                        ("assistant", answer)
                    )

                else:
                    error_msg = f"Error: {response.text}"

                    st.error(error_msg)

                    st.session_state.messages.append(
                        ("assistant", error_msg)
                    )

            except Exception as e:

                error_msg = f"Error: {str(e)}"

                st.error(error_msg)

                st.session_state.messages.append(
                    ("assistant", error_msg)
                )