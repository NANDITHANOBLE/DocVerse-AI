import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="DocVerse AI", page_icon="📄", layout="wide")

st.title("📄 DocVerse AI")
st.caption("Upload documents and chat with them using Groq + RAG")

# --- Session State Setup ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "collection_name" not in st.session_state:
    st.session_state.collection_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: Upload ---
with st.sidebar:
    st.header("Upload a Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Upload & Process"):
            with st.spinner("Uploading and processing document..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/upload", files=files)

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.collection_name = data["collection_name"]
                    st.session_state.messages = []
                    st.success(f"Uploaded! {data['num_chunks']} chunks created.")
                else:
                    st.error(f"Upload failed: {response.text}")

    if st.session_state.collection_name:
        st.info(f"Active document ID:\n`{st.session_state.collection_name}`")

    if st.button("🔄 Reset Chat"):
        requests.post(f"{API_URL}/chat/reset", params={"session_id": st.session_state.session_id})
        st.session_state.messages = []
        st.success("Chat history cleared.")

# --- Main Chat Area ---
if not st.session_state.collection_name:
    st.warning("👈 Please upload a PDF document from the sidebar to start chatting.")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask something about your document...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                payload = {
                    "session_id": st.session_state.session_id,
                    "collection_name": st.session_state.collection_name,
                    "message": user_input
                }
                response = requests.post(f"{API_URL}/chat", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    st.markdown(answer)

                    with st.expander("📚 Sources"):
                        for src in data["sources"]:
                            st.write(f"Page {src.get('page_label', 'N/A')}")

                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error: {response.text}")