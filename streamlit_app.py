import streamlit as st
import requests
import uuid
import os
import time
from datetime import datetime

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --- Page Config ---
st.set_page_config(
    page_title="DocVerse AI | Chat with Verse",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }

    /* ---- HEADER ---- */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 24px;
        background: rgba(127, 90, 240, 0.08);
        border: 1px solid #2a2a3d;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-logo {
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }
    .header-title {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #7F5AF0, #2CB67D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .header-subtitle {
        font-size: 0.8rem;
        color: #94A1B2;
        margin: 0;
    }
    .status-pill {
        display: flex;
        align-items: center;
        gap: 6px;
        background: rgba(44, 182, 125, 0.15);
        border: 1px solid #2CB67D;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 0.8rem;
        color: #2CB67D;
        font-weight: 600;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #2CB67D;
        box-shadow: 0 0 8px #2CB67D;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }
    .status-pill.offline {
        background: rgba(239, 68, 68, 0.15);
        border-color: #EF4444;
        color: #EF4444;
    }
    .status-pill.offline .status-dot {
        background: #EF4444;
        box-shadow: 0 0 8px #EF4444;
    }

    /* ---- SIDEBAR ---- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16161f 0%, #1a1a2e 100%);
        border-right: 1px solid #2a2a3d;
    }

    .stButton button {
        border-radius: 10px;
        border: 1px solid #7F5AF0;
        background: transparent;
        color: #7F5AF0;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: #7F5AF0;
        color: white;
        border-color: #7F5AF0;
        transform: translateY(-1px);
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    .stChatInput textarea {
        border-radius: 14px !important;
    }

    .doc-badge {
        background: rgba(127, 90, 240, 0.15);
        border: 1px solid #7F5AF0;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 0.85rem;
        color: #C4B5FD;
        margin-top: 10px;
    }

    .stat-box {
        background: rgba(255,255,255,0.03);
        border: 1px solid #2a2a3d;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
    }
    .stat-number {
        font-size: 1.3rem;
        font-weight: 700;
        color: #7F5AF0;
    }
    .stat-label {
        font-size: 0.7rem;
        color: #94A1B2;
        text-transform: uppercase;
    }

    hr {
        border-color: #2a2a3d;
    }

    .streamlit-expanderHeader {
        background-color: rgba(127, 90, 240, 0.08);
        border-radius: 10px;
    }

    /* ---- FOOTER ---- */
    .bottom-footer {
        margin-top: 40px;
        padding: 20px 10px;
        border-top: 1px solid #2a2a3d;
        text-align: center;
        color: #6B7280;
        font-size: 0.8rem;
    }
    .footer-badges {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 10px;
        flex-wrap: wrap;
    }
    .footer-badge {
        background: rgba(127, 90, 240, 0.1);
        border: 1px solid #2a2a3d;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.75rem;
        color: #94A1B2;
    }

    .timestamp {
        font-size: 0.7rem;
        color: #6B7280;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)

# --- Bot Persona ---
BOT_NAME = "Verse"
BOT_AVATAR = "🪐"
USER_AVATAR = "🧑‍💻"

# --- Session State Setup ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "collection_name" not in st.session_state:
    st.session_state.collection_name = None
if "doc_display_name" not in st.session_state:
    st.session_state.doc_display_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = 0

# --- Check Backend Status (Live Indicator) ---
def check_backend_status():
    try:
        r = requests.get(f"{API_URL}/", timeout=2)
        return r.status_code == 200
    except Exception:
        return False

backend_online = check_backend_status()

# --- HEADER ---
status_class = "status-pill" if backend_online else "status-pill offline"
status_text = "Backend Online" if backend_online else "Backend Offline"

st.markdown(f"""
<div class="top-header">
    <div class="header-left">
        <div class="header-logo">🪐</div>
        <div>
            <p class="header-title">DocVerse AI</p>
            <p class="header-subtitle">Chat with <b>{BOT_NAME}</b> — your AI document companion</p>
        </div>
    </div>
    <div class="{status_class}">
        <div class="status-dot"></div>
        {status_text}
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 📂 Document Hub")
    st.caption("Upload a PDF and let Verse read it for you.")

    uploaded_file = st.file_uploader("Drop your PDF here", type=["pdf"], label_visibility="collapsed")

    if uploaded_file is not None:
        if st.button("✨ Upload & Process", use_container_width=True):
            with st.spinner("🪄 Verse is reading your document..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{API_URL}/upload", files=files, timeout=120)

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.collection_name = data["collection_name"]
                        st.session_state.doc_display_name = uploaded_file.name
                        st.session_state.num_chunks = data.get("num_chunks", 0)
                        st.session_state.messages = []

                        if data.get("duplicate"):
                            st.warning("📎 Already uploaded — reusing existing data.")
                        else:
                            st.success(f"✅ Ready! {data['num_chunks']} chunks indexed.")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        try:
                            error_detail = response.json().get("detail", response.text)
                        except Exception:
                            error_detail = response.text
                        st.error(f"❌ {error_detail}")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Can't reach the backend. Is the FastAPI server running?")

    if st.session_state.collection_name:
        st.markdown(
            f'<div class="doc-badge">📄 <b>{st.session_state.doc_display_name or "Document"}</b><br>'
            f'<span style="opacity:0.7;">ID: {st.session_state.collection_name[:8]}...</span></div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="stat-box"><div class="stat-number">{st.session_state.num_chunks}</div><div class="stat-label">Chunks</div></div>', unsafe_allow_html=True)
        with c2:
            msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.markdown(f'<div class="stat-box"><div class="stat-number">{msg_count}</div><div class="stat-label">Questions</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Controls")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Chat", use_container_width=True):
            requests.post(f"{API_URL}/chat/reset", params={"session_id": st.session_state.session_id})
            st.session_state.messages = []
            st.rerun()

    with col2:
        if st.button("🗑️ Remove Doc", use_container_width=True):
            if st.session_state.collection_name:
                requests.delete(f"{API_URL}/document/{st.session_state.collection_name}")
                st.session_state.collection_name = None
                st.session_state.doc_display_name = None
                st.session_state.messages = []
                st.rerun()

    st.markdown("---")
    st.caption("💡 **Tip:** Ask follow-up questions — Verse remembers your last 10 messages!")

# --- Main Chat Area ---
if not st.session_state.collection_name:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px; opacity: 0.9;">
        <div style="font-size:4rem;">🪐</div>
        <h2>Hi, I'm Verse!</h2>
        <p style="font-size:1.1rem; color:#94A1B2;">
            Upload a PDF from the sidebar and I'll help you explore it —<br>
            ask me anything about its content, and I'll answer with real citations.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            st.markdown(f"Hey! I've finished reading **{st.session_state.doc_display_name}**. What would you like to know? 📖")

    for msg in st.session_state.messages:
        avatar = USER_AVATAR if msg["role"] == "user" else BOT_AVATAR
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                with st.expander("📚 View Sources"):
                    for src in msg["sources"]:
                        st.markdown(f"**📄 {src.get('file_name', 'Unknown')}** — Page {src.get('page_number', 'N/A')}")
                        st.caption(src.get('snippet', ''))
                        st.divider()
            if msg.get("timestamp"):
                st.markdown(f'<p class="timestamp">{msg["timestamp"]}</p>', unsafe_allow_html=True)

    user_input = st.chat_input(f"Ask {BOT_NAME} something about your document...")

    if user_input and not user_input.strip():
        st.warning("Please type a valid question.")
    elif user_input:
        now = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": now})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(user_input)
            st.markdown(f'<p class="timestamp">{now}</p>', unsafe_allow_html=True)

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            placeholder = st.empty()

            thinking_frames = ["💭 Thinking.", "💭 Thinking..", "💭 Thinking..."]
            for frame in thinking_frames * 2:
                placeholder.markdown(frame)
                time.sleep(0.15)

            try:
                payload = {
                    "session_id": st.session_state.session_id,
                    "collection_name": st.session_state.collection_name,
                    "message": user_input
                }
                response = requests.post(f"{API_URL}/chat", json=payload, timeout=60)

                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])

                    placeholder.markdown(answer)
                    reply_time = datetime.now().strftime("%I:%M %p")
                    st.markdown(f'<p class="timestamp">{reply_time}</p>', unsafe_allow_html=True)

                    if sources:
                        with st.expander("📚 View Sources"):
                            for src in sources:
                                st.markdown(f"**📄 {src.get('file_name', 'Unknown')}** — Page {src.get('page_number', 'N/A')}")
                                st.caption(src.get('snippet', ''))
                                st.divider()

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "timestamp": reply_time
                    })
                else:
                    try:
                        error_detail = response.json().get("detail", response.text)
                    except Exception:
                        error_detail = response.text
                    placeholder.error(f"❌ {error_detail}")

            except requests.exceptions.ConnectionError:
                placeholder.error("⚠️ Can't reach the backend. Is the FastAPI server running?")
            except requests.exceptions.Timeout:
                placeholder.error("⏱️ Request timed out. Try again.")

# --- FOOTER ---
st.markdown(f"""
<div class="bottom-footer">
    <p>🪐 <b>DocVerse AI</b> — Chat with your documents, powered by open-source AI</p>
    <div class="footer-badges">
        <span class="footer-badge">⚡ FastAPI</span>
        <span class="footer-badge">🦜 LangChain</span>
        <span class="footer-badge">🗄️ ChromaDB</span>
        <span class="footer-badge">🚀 Groq</span>
        <span class="footer-badge">🎨 Streamlit</span>
    </div>
    <p style="margin-top:10px; opacity:0.6;">Session ID: {st.session_state.session_id[:8]}... · © 2026 DocVerse AI</p>
</div>
""", unsafe_allow_html=True)