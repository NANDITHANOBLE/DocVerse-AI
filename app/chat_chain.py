from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.config import LLM_MODEL, GROQ_API_KEY
from app.vector_store import get_retriever
from app.memory_store import get_history, add_message

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

def chat_with_document(session_id: str, collection_name: str, question: str):
    retriever = get_retriever(collection_name)
    llm = get_llm()

    history = get_history(session_id)
    chat_history_messages = build_chat_history_messages(history)

    # Retrieve relevant chunks based on the question
    retrieved_docs = retriever.invoke(question)
    context = format_docs(retrieved_docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant answering questions based on the provided document context. "
                    "Use the context below to answer the user's question. "
                    "If the answer isn't in the context, say you don't know.\n\nContext:\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({
        "context": context,
        "chat_history": chat_history_messages,
        "question": question
    })

    add_message(session_id, "user", question)
    add_message(session_id, "assistant", answer)

    return {
        "answer": answer,
        "sources": [doc.metadata for doc in retrieved_docs]
    }