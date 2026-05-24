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
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("Upload PDFs")

    uploaded_files = st.file_uploader(
        "Choose PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        if st.button("Process PDFs"):

            with st.spinner("Uploading and processing PDFs..."):

                success = True

                for pdf in uploaded_files:

                    try:
                        files = {
                            "file": (
                                pdf.name,
                                pdf.getvalue(),
                                "application/pdf"
                            )
                        }

                        response = requests.post(
                            f"{BACKEND_URL}/upload-pdf",
                            files=files,
                            timeout=300
                        )

                        if response.status_code == 200:

                            if pdf.name not in st.session_state.uploaded_files:
                                st.session_state.uploaded_files.append(pdf.name)

                        else:
                            success = False
                            st.error(
                                f"Upload failed for {pdf.name}: {response.text}"
                            )

                    except Exception as e:
                        success = False
                        st.error(f"Error uploading {pdf.name}: {str(e)}")

                if success:
                    st.success("PDFs uploaded successfully!")

    st.subheader("Uploaded Documents")

    for file_name in st.session_state.uploaded_files:
        st.write(f"📄 {file_name}")

    if st.button("Reset PDFs"):

        st.session_state.uploaded_files = []
        st.session_state.messages = []

        st.rerun()

# -----------------------------
# MAIN UI
# -----------------------------
st.title("📄 AI PDF Chatbot")

# -----------------------------
# CHAT HISTORY
# -----------------------------
for role, message in st.session_state.messages:

    with st.chat_message(role):
        st.markdown(message)

# -----------------------------
# CHAT INPUT
# -----------------------------
question = st.chat_input("Ask a question about your PDFs")

if question:

    st.session_state.messages.append(("user", question))

    with st.chat_message("user"):
        st.markdown(question)

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