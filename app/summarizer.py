from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import LLM_MODEL, GROQ_API_KEY

def get_llm():
    return ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0
    )

def generate_document_overview(chunks, file_name: str, max_chunks_per_batch: int = 15):
    """
    Generates a structural overview of the entire document by processing
    chunks in batches and asking the LLM to extract a list of sections/topics
    (e.g., story titles) found in each batch, then combining them.
    """
    llm = get_llm()
    parser = StrOutputParser()

    extract_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are analyzing a document to build a table of contents. "
         "From the text below, extract ONLY the titles or names of distinct sections, "
         "stories, chapters, or topics you can identify (e.g., story titles in ALL CAPS or as headings). "
         "List them as a simple bullet list, one per line, in the order they appear. "
         "If no clear titles exist in this excerpt, respond with 'NONE'. "
         "Do not add commentary or explanations."),
        ("human", "{text}")
    ])
    extract_chain = extract_prompt | llm | parser

    all_titles = []
    batch_text = ""
    chunk_count = 0

    for chunk in chunks:
        batch_text += chunk.page_content + "\n\n"
        chunk_count += 1

        if chunk_count >= max_chunks_per_batch:
            result = extract_chain.invoke({"text": batch_text})
            if result.strip().upper() != "NONE":
                all_titles.append(result.strip())
            batch_text = ""
            chunk_count = 0

    # Process any remaining text
    if batch_text.strip():
        result = extract_chain.invoke({"text": batch_text})
        if result.strip().upper() != "NONE":
            all_titles.append(result.strip())

    combined_list = "\n".join(all_titles)

    # Final pass: clean up and deduplicate the combined list
    cleanup_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are given a raw list of section/story titles extracted from a document, possibly with duplicates "
         "or formatting inconsistencies. Clean this into a single, numbered, de-duplicated list, "
         "preserving the original order as much as possible. Output ONLY the numbered list, nothing else."),
        ("human", "{raw_list}")
    ])
    cleanup_chain = cleanup_prompt | llm | parser

    final_overview = cleanup_chain.invoke({"raw_list": combined_list})

    return {
        "file_name": file_name,
        "overview": final_overview,
        "total_chunks_processed": len(chunks)
    }

import json
import os
from app.config import OVERVIEWS_DIR

def save_overview(doc_id: str, overview_data: dict):
    path = os.path.join(OVERVIEWS_DIR, f"{doc_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(overview_data, f, ensure_ascii=False, indent=2)

def load_overview(doc_id: str):
    path = os.path.join(OVERVIEWS_DIR, f"{doc_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def overview_exists(doc_id: str) -> bool:
    path = os.path.join(OVERVIEWS_DIR, f"{doc_id}.json")
    return os.path.exists(path)