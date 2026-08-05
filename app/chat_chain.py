from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from fastapi import HTTPException

from app.config import LLM_MODEL, GROQ_API_KEY
from app.vector_store import get_retriever, keyword_search
from app.memory_store import get_history, add_message
from app.summarizer import load_overview, overview_exists

def get_llm():
    return ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0
    )

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_chat_history_messages(history: list):
    messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages

def build_sources(docs):
    """Builds a clean, de-duplicated list of source citations."""
    sources = []
    seen = set()

    for doc in docs:
        file_name = doc.metadata.get("file_name", "Unknown file")
        page_number = doc.metadata.get("page_number", "N/A")
        key = (file_name, page_number)

        if key not in seen:
            seen.add(key)
            snippet = doc.page_content[:200].strip()
            if len(doc.page_content) > 200:
                snippet += "..."

            sources.append({
                "file_name": file_name,
                "page_number": page_number,
                "snippet": snippet
            })

    return sources

STRUCTURAL_KEYWORDS = [
    "rank", "list all", "how many", "how much", "last story", "first story",
    "all stories", "all the stories", "table of contents", "list of stories",
    "which stories", "order of", "last one", "first one", "total number",
    "count the", "overview", "table of content", "list them", "name all",
    "list every", "all the", "every story"
]

def is_structural_question(question: str) -> bool:
    q = question.lower()
    return any(keyword in q for keyword in STRUCTURAL_KEYWORDS)

def chat_with_document(session_id: str, collection_name: str, question: str):
    # --- Retrieval step: combine semantic (MMR) + keyword search ---
    try:
        retriever = get_retriever(collection_name)
        semantic_docs = retriever.invoke(question)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Could not access this document. It may not exist or was deleted. ({str(e)})"
        )

    try:
        keyword_docs = keyword_search(collection_name, question, max_results=8)
    except Exception:
        keyword_docs = []

    seen_content = set()
    retrieved_docs = []
    for doc in semantic_docs + keyword_docs:
        if doc.page_content not in seen_content:
            seen_content.add(doc.page_content)
            retrieved_docs.append(doc)

    context = format_docs(retrieved_docs) if retrieved_docs else ""

    # --- Structural question handling: inject document overview ---
    overview_context = ""
    if is_structural_question(question) and overview_exists(collection_name):
        overview_data = load_overview(collection_name)
        if overview_data:
            overview_context = (
                f"\n\nDOCUMENT OVERVIEW (table of contents, in order as they appear in the document):\n"
                f"{overview_data.get('overview', '')}"
            )

    if not retrieved_docs and not overview_context:
        return {
            "answer": "I could not find any relevant information in this document to answer your question.",
            "sources": []
        }

    combined_context = context + overview_context

    history = get_history(session_id)
    chat_history_messages = build_chat_history_messages(history)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful assistant answering questions based on the provided document context, which contains excerpts from a collection of short stories. "
         "Each story typically ends with an explicit moral or lesson, sometimes stated directly (e.g., 'Moral: ...') and sometimes woven into the final sentences of the story. "
         "Carefully read through ALL the provided context before answering, as relevant information may appear in any part of it. "
         "If a DOCUMENT OVERVIEW section is provided, use it to answer questions about structure, order, counts, "
         "rankings, or lists of stories/sections — it reflects the true order and full list of contents in the document. "
         "If a specific story is mentioned by name in the context, use its concluding sentences to determine its moral or lesson. "
         "Answer directly and confidently based on what's in the context. "
         "If the context contains only partial information about a story, summarize confidently based on what is available without drawing attention to any gaps. "
         "Only say \"I could not find this information in the document\" if there is truly no relevant information anywhere in the context.\n\nContext:\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm | StrOutputParser()

        answer = chain.invoke({
            "context": combined_context,
            "chat_history": chat_history_messages,
            "question": question
        })
    except Exception as e:
        error_msg = str(e).lower()

        if "api_key" in error_msg or "authentication" in error_msg or "401" in error_msg:
            raise HTTPException(
                status_code=500,
                detail="Groq API authentication failed. Please check your GROQ_API_KEY in the .env file."
            )
        elif "rate limit" in error_msg or "429" in error_msg:
            raise HTTPException(
                status_code=429,
                detail="Groq API rate limit reached. Please wait a moment and try again."
            )
        elif "timeout" in error_msg or "connection" in error_msg:
            raise HTTPException(
                status_code=503,
                detail="Could not connect to the Groq API. Please check your internet connection and try again."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while generating the answer: {str(e)}"
            )

    add_message(session_id, "user", question)
    add_message(session_id, "assistant", answer)

    return {
        "answer": answer,
        "sources": build_sources(retrieved_docs)
    }